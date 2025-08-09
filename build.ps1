#!/usr/bin/env pwsh
#Requires -Version 7.0

<#
.SYNOPSIS
    Private build script for the Python Game Solution
.DESCRIPTION
    This script performs a complete build pipeline including:
    - Environment cleanup
    - Code compilation/validation
    - Unit, integration, and system testing
    - Code coverage analysis
    - Package creation for distribution
.PARAMETER SkipTests
    Skip all test execution (useful for quick builds)
.PARAMETER SkipPackaging
    Skip the packaging step
.PARAMETER Clean
    Perform only cleanup operations
.EXAMPLE
    .\build.ps1
    Run the complete build pipeline
.EXAMPLE
    .\build.ps1 -SkipTests
    Build without running tests
.EXAMPLE
    .\build.ps1 -Clean
    Clean up temporary files only
#>

[CmdletBinding()]
param(
    [switch]$SkipTests,
    [switch]$SkipPackaging,
    [switch]$Clean
)

# Script configuration
$ErrorActionPreference = "Stop"
$VerbosePreference = if ($VerbosePreference -eq "Continue") { "Continue" } else { "SilentlyContinue" }

# Build configuration
$BuildConfig = @{
    ProjectRoot = $PSScriptRoot
    SourceDir = Join-Path $PSScriptRoot "src"
    TestsDir = Join-Path $PSScriptRoot "tests"
    OutputDir = Join-Path $PSScriptRoot "dist"
    CoverageDir = Join-Path $PSScriptRoot "htmlcov"
    VenvDir = Join-Path $PSScriptRoot ".venv"
    PackageName = "tic-tac-toe-game"
    Version = "1.0.0"
    PythonExecutable = if ($IsWindows) { 
        Join-Path $PSScriptRoot ".venv\Scripts\python.exe" 
    } else { 
        Join-Path $PSScriptRoot ".venv/bin/python" 
    }
}

# Logging functions
function Write-BuildStep {
    param([string]$Message)
    Write-Host "🔨 $Message" -ForegroundColor Cyan
}

function Write-BuildSuccess {
    param([string]$Message)
    Write-Host "✅ $Message" -ForegroundColor Green
}

function Write-BuildError {
    param([string]$Message)
    Write-Host "❌ $Message" -ForegroundColor Red
}

function Write-BuildWarning {
    param([string]$Message)
    Write-Host "⚠️  $Message" -ForegroundColor Yellow
}

function Write-BuildInfo {
    param([string]$Message)
    Write-Host "ℹ️  $Message" -ForegroundColor Blue
}

# Utility functions
function Test-PythonVirtualEnvironment {
    if (-not (Test-Path $BuildConfig.PythonExecutable)) {
        Write-BuildError "Python virtual environment not found at: $($BuildConfig.PythonExecutable)"
        Write-BuildInfo "Please ensure the virtual environment is set up correctly."
        return $false
    }
    return $true
}

function Invoke-BuildCommand {
    param(
        [string]$Command,
        [string]$WorkingDirectory = $BuildConfig.ProjectRoot,
        [string]$Description = "Running command"
    )
    
    Write-Verbose "$Description`: $Command"
    
    try {
        $process = Start-Process -FilePath "cmd.exe" -ArgumentList "/c", $Command -WorkingDirectory $WorkingDirectory -Wait -PassThru -NoNewWindow
        if ($process.ExitCode -ne 0) {
            throw "Command failed with exit code $($process.ExitCode)"
        }
    }
    catch {
        Write-BuildError "$Description failed: $($_.Exception.Message)"
        throw
    }
}

function Remove-BuildArtifacts {
    Write-BuildStep "Cleaning up build artifacts and temporary files"
    
    $pathsToClean = @(
        ".pytest_cache",
        "__pycache__",
        "*.pyc",
        "*.pyo",
        "*.pyd",
        ".coverage",
        "coverage.xml",
        "htmlcov",
        "dist",
        "build",
        "*.egg-info",
        ".mypy_cache",
        ".tox",
        "node_modules"
    )
    
    foreach ($pattern in $pathsToClean) {
        $itemsToRemove = Get-ChildItem -Path $BuildConfig.ProjectRoot -Recurse -Force -Name $pattern -ErrorAction SilentlyContinue
        foreach ($item in $itemsToRemove) {
            $fullPath = Join-Path $BuildConfig.ProjectRoot $item
            if (Test-Path $fullPath) {
                Write-Verbose "Removing: $fullPath"
                Remove-Item -Path $fullPath -Recurse -Force -ErrorAction SilentlyContinue
            }
        }
    }
    
    Write-BuildSuccess "Cleanup completed"
}

function Test-CodeQuality {
    Write-BuildStep "Running code quality checks"
    
    # Python syntax check
    Write-BuildInfo "Checking Python syntax..."
    $pyFiles = Get-ChildItem -Path $BuildConfig.SourceDir -Recurse -Filter "*.py"
    foreach ($file in $pyFiles) {
        Invoke-BuildCommand -Command "$($BuildConfig.PythonExecutable) -m py_compile `"$($file.FullName)`"" -Description "Syntax check for $($file.Name)"
    }
    
    # Import validation
    Write-BuildInfo "Validating imports..."
    Invoke-BuildCommand -Command "$($BuildConfig.PythonExecutable) -c `"import sys; sys.path.insert(0, 'src'); import tic_tac_toe.app`"" -Description "Import validation"
    
    Write-BuildSuccess "Code quality checks passed"
}

function Invoke-UnitTests {
    Write-BuildStep "Running unit tests"
    
    $testCommand = "$($BuildConfig.PythonExecutable) -m pytest tests/unit/ --cov=src --cov-report=term-missing --cov-report=html:htmlcov/unit --cov-report=xml:coverage-unit.xml -v --tb=short"
    
    try {
        Invoke-BuildCommand -Command $testCommand -Description "Unit tests"
        Write-BuildSuccess "Unit tests passed"
        return $true
    }
    catch {
        Write-BuildError "Unit tests failed"
        return $false
    }
}

function Invoke-IntegrationTests {
    Write-BuildStep "Running integration tests"
    
    $testCommand = "$($BuildConfig.PythonExecutable) -m pytest tests/integration/ --cov=src --cov-append --cov-report=term-missing --cov-report=html:htmlcov/integration --cov-report=xml:coverage-integration.xml -v --tb=short"
    
    try {
        Invoke-BuildCommand -Command $testCommand -Description "Integration tests"
        Write-BuildSuccess "Integration tests passed"
        return $true
    }
    catch {
        Write-BuildError "Integration tests failed"
        return $false
    }
}

function Invoke-SystemTests {
    Write-BuildStep "Running system tests"
    
    # Run fast system tests first
    $fastTestCommand = "$($BuildConfig.PythonExecutable) -m pytest tests/system/ -k `"not slow`" --cov=src --cov-append --cov-report=term-missing --cov-report=html:htmlcov/system --cov-report=xml:coverage-system.xml -v --tb=short"
    
    try {
        Invoke-BuildCommand -Command $fastTestCommand -Description "System tests (fast)"
        
        # Run slow system tests
        Write-BuildInfo "Running performance and slow system tests..."
        $slowTestCommand = "$($BuildConfig.PythonExecutable) -m pytest tests/system/ -k `"slow`" --cov=src --cov-append --cov-report=term-missing --tb=short"
        Invoke-BuildCommand -Command $slowTestCommand -Description "System tests (slow)"
        
        Write-BuildSuccess "System tests passed"
        return $true
    }
    catch {
        Write-BuildError "System tests failed"
        return $false
    }
}

function New-CoverageReport {
    Write-BuildStep "Generating comprehensive code coverage report"
    
    try {
        # Generate combined coverage report
        $coverageCommand = "$($BuildConfig.PythonExecutable) -m pytest tests/ --cov=src --cov-report=term-missing --cov-report=html:htmlcov/combined --cov-report=xml:coverage-combined.xml --tb=no -q"
        Invoke-BuildCommand -Command $coverageCommand -Description "Combined coverage report"
        
        # Display coverage summary
        if (Test-Path "coverage-combined.xml") {
            Write-BuildInfo "Coverage reports generated:"
            Write-BuildInfo "  - HTML Report: htmlcov/combined/index.html"
            Write-BuildInfo "  - XML Report: coverage-combined.xml"
            
            # Parse and display coverage percentage
            try {
                $coverageXml = [xml](Get-Content "coverage-combined.xml")
                $coveragePercent = [math]::Round([double]$coverageXml.coverage.'line-rate' * 100, 2)
                Write-BuildInfo "  - Total Coverage: $coveragePercent%"
                
                if ($coveragePercent -ge 80) {
                    Write-BuildSuccess "Excellent code coverage: $coveragePercent%"
                } elseif ($coveragePercent -ge 60) {
                    Write-BuildWarning "Good code coverage: $coveragePercent% (consider improving to 80%+)"
                } else {
                    Write-BuildWarning "Low code coverage: $coveragePercent% (should be 60%+)"
                }
            }
            catch {
                Write-BuildWarning "Could not parse coverage percentage from XML report"
            }
        }
        
        Write-BuildSuccess "Coverage report generation completed"
        return $true
    }
    catch {
        Write-BuildError "Coverage report generation failed"
        return $false
    }
}

function New-DistributionPackage {
    Write-BuildStep "Creating distribution package"
    
    # Create output directory
    $null = New-Item -Path $BuildConfig.OutputDir -ItemType Directory -Force
    
    try {
        # Create package structure
        $packageDir = Join-Path $BuildConfig.OutputDir $BuildConfig.PackageName
        $null = New-Item -Path $packageDir -ItemType Directory -Force
        
        # Copy source files
        Write-BuildInfo "Copying source files..."
        Copy-Item -Path $BuildConfig.SourceDir -Destination $packageDir -Recurse -Force
        
        # Copy main entry point
        Copy-Item -Path (Join-Path $BuildConfig.ProjectRoot "app.py") -Destination $packageDir -Force
        
        # Copy requirements
        if (Test-Path (Join-Path $BuildConfig.ProjectRoot "requirements.txt")) {
            Copy-Item -Path (Join-Path $BuildConfig.ProjectRoot "requirements.txt") -Destination $packageDir -Force
        }
        
        # Copy README and documentation
        $docFiles = @("README.md", "SYSTEM_TEST_SUITE_DOCUMENTATION.md")
        foreach ($docFile in $docFiles) {
            $docPath = Join-Path $BuildConfig.ProjectRoot $docFile
            if (Test-Path $docPath) {
                Copy-Item -Path $docPath -Destination $packageDir -Force
            }
        }
        
        # Create run script for Windows
        $runScript = @"
@echo off
echo Starting Tic-Tac-Toe Game...
echo.
python app.py
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Error: Failed to start the game.
    echo Please ensure Python is installed and requirements are met.
    pause
)
"@
        $runScript | Out-File -FilePath (Join-Path $packageDir "run.bat") -Encoding ascii
        
        # Create PowerShell run script
        $psRunScript = @"
#!/usr/bin/env pwsh
Write-Host "Starting Tic-Tac-Toe Game..." -ForegroundColor Green
try {
    python app.py
}
catch {
    Write-Host "Error: Failed to start the game." -ForegroundColor Red
    Write-Host "Please ensure Python is installed and requirements are met." -ForegroundColor Yellow
    Read-Host "Press Enter to continue"
}
"@
        $psRunScript | Out-File -FilePath (Join-Path $packageDir "run.ps1") -Encoding utf8
        
        # Create installation instructions
        $instructions = @"
# Tic-Tac-Toe Game - Installation Instructions

## Prerequisites
- Python 3.9 or higher
- pip (Python package installer)

## Installation
1. Extract this package to a directory of your choice
2. Open a terminal/command prompt in the extracted directory
3. Install required dependencies:
   ``````
   pip install -r requirements.txt
   ``````

## Running the Game
- **Windows**: Double-click `run.bat` or run `python app.py`
- **PowerShell**: Run `.\run.ps1`
- **Command Line**: Run `python app.py`

## Game Features
- Interactive Tic-Tac-Toe gameplay
- Mouse click controls
- Visual game board
- Win/tie detection
- Game restart functionality

## Troubleshooting
If you encounter issues:
1. Ensure Python is installed and in your PATH
2. Verify all requirements are installed: `pip list`
3. Check that you're in the correct directory
4. Try running `python app.py` directly

Version: $($BuildConfig.Version)
Build Date: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')
"@
        $instructions | Out-File -FilePath (Join-Path $packageDir "INSTALL.md") -Encoding utf8
        
        # Create ZIP package
        Write-BuildInfo "Creating ZIP archive..."
        $zipPath = Join-Path $BuildConfig.OutputDir "$($BuildConfig.PackageName)-v$($BuildConfig.Version).zip"
        
        if (Test-Path $zipPath) {
            Remove-Item $zipPath -Force
        }
        
        # Use .NET compression for PowerShell 7 compatibility
        Add-Type -AssemblyName System.IO.Compression.FileSystem
        [System.IO.Compression.ZipFile]::CreateFromDirectory($packageDir, $zipPath)
        
        # Calculate file size
        $zipSize = [math]::Round((Get-Item $zipPath).Length / 1MB, 2)
        
        Write-BuildSuccess "Distribution package created successfully"
        Write-BuildInfo "Package Location: $zipPath"
        Write-BuildInfo "Package Size: $zipSize MB"
        Write-BuildInfo "Package Contents:"
        Write-BuildInfo "  - Source code (src/)"
        Write-BuildInfo "  - Main application (app.py)"
        Write-BuildInfo "  - Run scripts (run.bat, run.ps1)"
        Write-BuildInfo "  - Installation guide (INSTALL.md)"
        Write-BuildInfo "  - Documentation and requirements"
        
        return $true
    }
    catch {
        Write-BuildError "Package creation failed: $($_.Exception.Message)"
        return $false
    }
}

function Show-BuildSummary {
    param(
        [bool]$TestsPassed,
        [bool]$CoverageGenerated,
        [bool]$PackageCreated,
        [datetime]$StartTime
    )
    
    $duration = (Get-Date) - $StartTime
    
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Magenta
    Write-Host "BUILD SUMMARY" -ForegroundColor Magenta
    Write-Host "========================================" -ForegroundColor Magenta
    
    Write-Host "Build Duration: $($duration.ToString('mm\:ss'))" -ForegroundColor White
    Write-Host ""
    
    if ($TestsPassed) {
        Write-BuildSuccess "✅ All Tests Passed"
    } else {
        Write-BuildError "❌ Tests Failed"
    }
    
    if ($CoverageGenerated) {
        Write-BuildSuccess "✅ Coverage Report Generated"
    } else {
        Write-BuildWarning "⚠️  Coverage Report Not Generated"
    }
    
    if ($PackageCreated) {
        Write-BuildSuccess "✅ Distribution Package Created"
    } else {
        Write-BuildWarning "⚠️  Distribution Package Not Created"
    }
    
    Write-Host ""
    
    if ($TestsPassed -and $CoverageGenerated -and ($PackageCreated -or $SkipPackaging)) {
        Write-BuildSuccess "🎉 BUILD SUCCEEDED!"
    } else {
        Write-BuildError "💥 BUILD FAILED!"
        exit 1
    }
}

# Main build pipeline
function Start-Build {
    $startTime = Get-Date
    $testsPassed = $false
    $coverageGenerated = $false
    $packageCreated = $false
    
    Write-Host "🚀 Starting build pipeline..." -ForegroundColor Magenta
    Write-Host "Project: $($BuildConfig.PackageName)" -ForegroundColor White
    Write-Host "Version: $($BuildConfig.Version)" -ForegroundColor White
    Write-Host "Root: $($BuildConfig.ProjectRoot)" -ForegroundColor White
    Write-Host ""
    
    try {
        # Step 1: Environment validation
        Write-BuildStep "Validating build environment"
        if (-not (Test-PythonVirtualEnvironment)) {
            throw "Build environment validation failed"
        }
        Write-BuildSuccess "Environment validation passed"
        
        # Step 2: Cleanup
        Remove-BuildArtifacts
        
        if ($Clean) {
            Write-BuildSuccess "Cleanup completed (Clean mode)"
            Write-Host ""
            Write-Host "========================================" -ForegroundColor Magenta
            Write-Host "CLEANUP SUMMARY" -ForegroundColor Magenta
            Write-Host "========================================" -ForegroundColor Magenta
            Write-BuildSuccess "🧹 CLEANUP SUCCEEDED!"
            return
        }
        
        # Step 3: Code quality checks
        Test-CodeQuality
        
        # Step 4: Testing pipeline
        if (-not $SkipTests) {
            Write-BuildStep "Starting test execution pipeline"
            
            $unitTestsOk = Invoke-UnitTests
            $integrationTestsOk = Invoke-IntegrationTests
            $systemTestsOk = Invoke-SystemTests
            
            $testsPassed = $unitTestsOk -and $integrationTestsOk -and $systemTestsOk
            
            if ($testsPassed) {
                Write-BuildSuccess "All test suites passed"
            } else {
                Write-BuildError "One or more test suites failed"
                Write-BuildInfo "Unit Tests: $(if($unitTestsOk){'✅'}else{'❌'})"
                Write-BuildInfo "Integration Tests: $(if($integrationTestsOk){'✅'}else{'❌'})"
                Write-BuildInfo "System Tests: $(if($systemTestsOk){'✅'}else{'❌'})"
            }
            
            # Step 5: Coverage report (run even if tests failed for debugging)
            $coverageGenerated = New-CoverageReport
        } else {
            Write-BuildWarning "Skipping tests (SkipTests flag enabled)"
            $testsPassed = $true  # Assume success when skipping
            $coverageGenerated = $true
        }
        
        # Step 6: Packaging
        if (-not $SkipPackaging -and ($testsPassed -or $SkipTests)) {
            $packageCreated = New-DistributionPackage
        } else {
            if ($SkipPackaging) {
                Write-BuildWarning "Skipping packaging (SkipPackaging flag enabled)"
                $packageCreated = $true  # Assume success when skipping
            } else {
                Write-BuildWarning "Skipping packaging due to test failures"
            }
        }
        
    }
    catch {
        Write-BuildError "Build pipeline failed: $($_.Exception.Message)"
        Write-BuildError "Stack trace: $($_.ScriptStackTrace)"
    }
    finally {
        Show-BuildSummary -TestsPassed $testsPassed -CoverageGenerated $coverageGenerated -PackageCreated $packageCreated -StartTime $startTime
    }
}

# Script entry point
if ($MyInvocation.InvocationName -ne '.') {
    Start-Build
}
