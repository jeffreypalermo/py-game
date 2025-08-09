# Build Script Documentation

## Overview
The `build.ps1` script is a comprehensive PowerShell 7 build pipeline for the Python Game Solution. It automates the complete build, test, and packaging process.

## Prerequisites
- **PowerShell 7** (`pwsh`) - Required for script execution
- **Python Virtual Environment** - Must be set up at `.venv/`
- **Python Dependencies** - All requirements installed in virtual environment

## Usage

### Basic Commands

```powershell
# Complete build pipeline (recommended)
.\build.ps1

# Clean only (remove temp files and artifacts)
.\build.ps1 -Clean

# Build without tests (faster for development)
.\build.ps1 -SkipTests

# Build without packaging
.\build.ps1 -SkipPackaging

# Verbose output for debugging
.\build.ps1 -Verbose
```

### Combination Options

```powershell
# Quick build for development
.\build.ps1 -SkipTests -SkipPackaging

# Clean build with verbose output
.\build.ps1 -Clean -Verbose
```

## Build Pipeline Stages

### 1. 🔨 Environment Validation
- Verifies Python virtual environment exists
- Checks required executables are available

### 2. 🧹 Cleanup
- Removes build artifacts (`.pytest_cache`, `__pycache__`, etc.)
- Cleans up coverage reports and temporary files
- Removes distribution directories

### 3. ✅ Code Quality Checks
- Python syntax validation for all source files
- Import validation to ensure code compiles
- Module import testing

### 4. 🧪 Test Execution Pipeline
- **Unit Tests**: Fast, isolated component tests (57 tests)
- **Integration Tests**: Cross-component interaction tests (5 tests)
- **System Tests**: Complete end-to-end scenarios (56 tests)
- **Performance Tests**: Slow/load testing scenarios (4 tests)

### 5. 📊 Coverage Analysis
- Generates comprehensive code coverage reports
- Creates HTML reports for visual analysis
- Produces XML reports for CI/CD integration
- **Current Coverage**: ~71% (Good - consider improving to 80%+)

### 6. 📦 Distribution Packaging
- Creates deployable ZIP package
- Includes source code, entry point, and documentation
- Generates Windows batch and PowerShell run scripts
- Creates installation instructions

## Output Artifacts

### Test Reports
- `htmlcov/unit/` - Unit test coverage HTML report
- `htmlcov/integration/` - Integration test coverage HTML report  
- `htmlcov/system/` - System test coverage HTML report
- `htmlcov/combined/` - Combined coverage HTML report
- `coverage-*.xml` - XML coverage reports for CI/CD

### Distribution Package
- `dist/tic-tac-toe-game-v1.0.0.zip` - Complete distributable package
- `dist/tic-tac-toe-game/` - Unpackaged distribution folder

### Package Contents
- **Source Code**: Complete `src/` directory with all modules
- **Entry Point**: `app.py` - Main application launcher
- **Run Scripts**: 
  - `run.bat` - Windows batch file
  - `run.ps1` - PowerShell script
- **Documentation**:
  - `README.md` - Project overview
  - `INSTALL.md` - Installation instructions
  - `SYSTEM_TEST_SUITE_DOCUMENTATION.md` - Test documentation
- **Requirements**: `requirements.txt` - Python dependencies

## Build Success Criteria

✅ **All Tests Pass**
- Unit Tests: 57/57 ✅
- Integration Tests: 5/5 ✅ 
- System Tests: 56/56 ✅

✅ **Code Coverage**
- Minimum: 60% (Warning threshold)
- Good: 71% (Current achievement)
- Excellent: 80%+ (Target)

✅ **Package Creation**
- ZIP file created successfully
- All required files included
- Package size reasonable (<1MB)

## Error Handling

The script provides clear error messages and color-coded output:
- 🔨 **Blue**: Build step information
- ✅ **Green**: Success messages
- ⚠️ **Yellow**: Warnings
- ❌ **Red**: Errors and failures

## Performance

Typical build times:
- **Clean Only**: ~30 seconds
- **Skip Tests**: ~45 seconds
- **Complete Build**: ~1-2 minutes
- **With Packaging**: +15 seconds

## Troubleshooting

### Common Issues

1. **"PowerShell 7 Required"**
   ```
   Solution: Install PowerShell 7 (pwsh) and use 'pwsh' instead of 'powershell'
   ```

2. **"Virtual Environment Not Found"**
   ```
   Solution: Ensure .venv/ directory exists with proper Python installation
   ```

3. **"Test Failures"**
   ```
   Solution: Review test output, fix failing tests, then re-run build
   ```

### Debug Mode
Use `-Verbose` flag for detailed output and troubleshooting information.

## Integration

The build script is designed for:
- **Local Development**: Quick validation and testing
- **CI/CD Pipelines**: Automated build and deployment
- **Release Preparation**: Package creation for distribution

## Version History

- **v1.0.0**: Initial comprehensive build pipeline
  - Complete test automation
  - Coverage reporting
  - Distribution packaging
  - Cross-platform support (Windows focus)

---

*For more information about the game itself, see the main [README.md](README.md)*
