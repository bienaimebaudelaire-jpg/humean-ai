<#
.SYNOPSIS
    Rotation automatique des clés HUMEAN - Sécurité systémique
.DESCRIPTION
    Génère une nouvelle paire Ed25519 tous les 30 jours
    Met à jour la configuration multisig
    Archive l'ancienne clé
#>

param(
    [switch]$Force = $false
)

# Configuration
$KEY_DIR = ".\attestation"
$LEDGER_DIR = ".\log" 
$MULTISIG_CONFIG = ".\attestation\multisig_config.json"
$KEY_ROTATION_DAYS = 30

# Crée les dossiers si nécessaire
if (-not (Test-Path $KEY_DIR)) { mkdir $KEY_DIR -Force }
if (-not (Test-Path $LEDGER_DIR)) { mkdir $LEDGER_DIR -Force }

# Fonction de génération de clé Ed25519
function New-Ed25519KeyPair {
    $keyName = "PRIMARY-KEY-$(Get-Date -Format 'yyyyMMdd-HHmmss')"
    
    # Génère une paire de clés (simulation - en production utiliser une lib crypto)
    $privateKey = [System.Convert]::ToBase64String((1..32 | ForEach-Object { Get-Random -Maximum 256 }))
    $publicKey = [System.Convert]::ToBase64String((1..32 | ForEach-Object { Get-Random -Maximum 256 }))
    
    return @{
        Name = $keyName
        Private = $privateKey
        Public = $publicKey
        Created = (Get-Date -Format "yyyy-MM-ddTHH:mm:ssZ")
    }
}

# Vérifie si la rotation est nécessaire
function Test-KeyRotationNeeded {
    $currentKey = Get-ChildItem "$KEY_DIR\PRIMARY-KEY-*.pub.b64" | Sort-Object LastWriteTime | Select-Object -Last 1
    
    if (-not $currentKey) {
        Write-Host "?? Aucune clé trouvée - création initiale requise"
        return $true
    }
    
    $keyAge = (Get-Date) - $currentKey.LastWriteTime
    $needsRotation = $keyAge.Days -ge $KEY_ROTATION_DAYS
    
    if ($needsRotation) {
        Write-Host "?? Rotation nécessaire : clé âgée de $($keyAge.Days) jours"
    } else {
        Write-Host "? Clé à jour : $($keyAge.Days) jours sur $KEY_ROTATION_DAYS"
    }
    
    return $needsRotation -or $Force
}

# Crée la configuration multisig
function Initialize-MultisigConfig {
    if (-not (Test-Path $MULTISIG_CONFIG)) {
        Write-Host "?? Création configuration multisig..."
        
        $multisigConfig = @{
            version = "1.0"
            created = (Get-Date -Format "yyyy-MM-ddTHH:mm:ssZ")
            policy = @{
                required_signatures = 2
                max_keys = 5
                rotation_days = $KEY_ROTATION_DAYS
            }
            signatories = @()
            key_history = @()
        }
        
        $multisigConfig | ConvertTo-Json -Depth 5 | Set-Content $MULTISIG_CONFIG -Encoding UTF8
    }
    
    return Get-Content $MULTISIG_CONFIG | ConvertFrom-Json
}

# Rotation principale
function Invoke-KeyRotation {
    Write-Host "?? DÉBUT ROTATION DES CLÉS HUMEAN" -ForegroundColor Cyan
    
    # Vérifie si nécessaire
    if (-not (Test-KeyRotationNeeded)) {
        Write-Host "??  Rotation non nécessaire" -ForegroundColor Yellow
        return
    }
    
    # Charge la config multisig
    $multisigConfig = Initialize-MultisigConfig
    
    # Génère nouvelle paire de clés
    Write-Host "?? Génération nouvelle paire Ed25519..."
    $newKey = New-Ed25519KeyPair
    
    # Sauvegarde les clés
    $newKey.Private | Set-Content "$KEY_DIR\$($newKey.Name).priv.b64" -Encoding UTF8
    $newKey.Public | Set-Content "$KEY_DIR\$($newKey.Name).pub.b64" -Encoding UTF8
    
    # Met à jour la configuration multisig
    $signatory = @{
        key_name = $newKey.Name
        public_key = $newKey.Public
        activated = (Get-Date -Format "yyyy-MM-ddTHH:mm:ssZ")
        status = "active"
    }
    
    $multisigConfig.signatories = @($signatory) + $multisigConfig.signatories
    $multisigConfig.key_history += @{
        key_name = $newKey.Name
        activated = $signatory.activated
        retired = $null
        status = "active"
    }
    
    # Désactive les anciennes clés (garder les 2 plus récentes)
    $activeKeys = $multisigConfig.signatories | Where-Object { $_.status -eq "active" }
    if ($activeKeys.Count -gt 2) {
        $keysToRetire = $activeKeys | Select-Object -Skip 2
        foreach ($key in $keysToRetire) {
            $key.status = "retired"
            $historyEntry = $multisigConfig.key_history | Where-Object { $_.key_name -eq $key.key_name }
            if ($historyEntry) {
                $historyEntry.retired = (Get-Date -Format "yyyy-MM-ddTHH:mm:ssZ")
                $historyEntry.status = "retired"
            }
        }
    }
    
    # Sauvegarde la config
    $multisigConfig | ConvertTo-Json -Depth 5 | Set-Content $MULTISIG_CONFIG -Encoding UTF8
    
    # Crée une entrée de ledger
    $ledgerEntry = @{
        event = "key_rotation"
        timestamp = (Get-Date -Format "yyyy-MM-ddTHH:mm:ssZ")
        new_key = $newKey.Name
        active_signatories = ($multisigConfig.signatories | Where-Object { $_.status -eq "active" }).Count
        required_signatures = $multisigConfig.policy.required_signatures
    }
    
    $ledgerEntry | ConvertTo-Json -Depth 3 | Add-Content "$LEDGER_DIR\ledger_signed.jsonl" -Encoding UTF8
    
    Write-Host "? ROTATION TERMINÉE" -ForegroundColor Green
    Write-Host "   Nouvelle clé : $($newKey.Name)"
    Write-Host "   Signataires actifs : $(($multisigConfig.signatories | Where-Object { $_.status -eq 'active' }).Count)"
    Write-Host "   Signatures requises : $($multisigConfig.policy.required_signatures)"
}

# Exécution
try {
    Invoke-KeyRotation
} catch {
    Write-Host "? ERREUR : $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}
