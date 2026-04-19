# Install ont CLI globally via pipx (Windows PowerShell)
# Run as: .\install.ps1

$RepoDir = Split-Path -Parent $MyInvocation.MyCommand.Path

if (-not (Get-Command pipx -ErrorAction SilentlyContinue)) {
    Write-Host "pipx not found. Installing..."
    python -m pip install --user pipx
    python -m pipx ensurepath
    Write-Host "Restart PowerShell for PATH changes to take effect."
    exit 0
}

Write-Host "Installing ont from $RepoDir ..."
pipx install --editable $RepoDir

Write-Host ""
Write-Host "Done. Run: ont --help"
