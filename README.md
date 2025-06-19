# Playwright UI Test Framework Template

## Selenoid Integration

This framework supports running tests against Selenoid, which provides browsers in Docker containers.

### Setting Up Selenoid

#### Local Setup

1. **Install Docker**
   
   Make sure Docker is installed and running on your system.

2. **Install Configuration Manager**
   
   For Linux/macOS:
   ```bash
   curl -s https://aerokube.com/cm/bash | bash
   ```
   
   For Windows:
   ```powershell
   curl -o cm.exe https://github.com/aerokube/cm/releases/download/1.8.5/cm_windows_amd64.exe
   ```

3. **Start Selenoid**
   
   ```bash
   ./cm selenoid start --vnc
   ```
   
   This will pull necessary browser images and start Selenoid with VNC support.

4. **Start Selenoid UI (Optional)**
   
   ```bash
   ./cm selenoid-ui start
   ```
   
   Access Selenoid UI at http://localhost:8080 to monitor test execution.

#### Jenkins Integration

Add the following to your Jenkinsfile:

```groovy
stage('Setup Selenoid') {
    steps {
        sh '''
            curl -s https://aerokube.com/cm/bash > cm
            chmod +x cm
            ./cm selenoid start --vnc
        '''
    }
}
```

### Running Tests with Selenoid

To run tests against Selenoid:

```bash
pytest --selenoid-url="http://localhost:4444/wd/hub" --browser-type=chromium --browser-version=latest --resolution=fhd
```

Available options:
- `--selenoid-url`: URL of your Selenoid instance
- `--browser-type`: Browser type (chromium, firefox, webkit, edge)
- `--browser-version`: Browser version to use (default: latest)
- `--resolution`: Screen resolution (hd, fhd, qhd, uhd, fullscreen)

Note: When using with Selenoid, WebKit is mapped to Chrome as Selenoid doesn't directly support WebKit.

## Browser Support

The framework supports the following browsers:

- **Chromium**: The open-source browser that powers Chrome
- **Firefox**: Mozilla's web browser
- **WebKit**: The engine that powers Safari
- **Edge**: Microsoft's Chromium-based browser

### Using Microsoft Edge

To run tests with Microsoft Edge:

```bash
pytest --browser-type=edge --target="https://example.com"
```

For local execution, this requires Microsoft Edge to be installed on your system. When running with Selenoid, ensure that Edge browser images are available in your Selenoid setup.