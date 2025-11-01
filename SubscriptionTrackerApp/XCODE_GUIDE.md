# iOS App Development Guide

This guide provides instructions for opening and building the Subscription Tracker iOS app in Xcode.

## Prerequisites

- macOS with Xcode 15.0 or later
- iOS 16.0+ device or simulator

## Opening the Project in Xcode

Since this is a Swift Package Manager project, there are multiple ways to open it in Xcode:

### Method 1: Open Package.swift directly

1. Navigate to the `SubscriptionTrackerApp` folder
2. Double-click `Package.swift` or right-click and select "Open with Xcode"
3. Xcode will automatically resolve dependencies and open the project

### Method 2: Open from Xcode

1. Open Xcode
2. Select "File" → "Open..."
3. Navigate to and select the `SubscriptionTrackerApp` folder
4. Click "Open"

## Building the iOS App

Due to the SwiftUI dependency in the UI layer, the complete iOS app can only be built on macOS with Xcode:

### Building for iOS Simulator

1. Open the project in Xcode (see above)
2. Select an iOS simulator from the device dropdown (e.g., "iPhone 15 Pro")
3. Press `Cmd+B` to build or `Cmd+R` to build and run
4. The app will launch in the simulator

### Building for Physical Device

1. Connect your iOS device to your Mac
2. In Xcode, select your device from the device dropdown
3. Configure code signing:
   - Select the project in the navigator
   - Go to "Signing & Capabilities"
   - Select your team/account
4. Press `Cmd+R` to build and run on your device

## Creating an App Target

To create a proper iOS app target (rather than just a library):

1. Open the project in Xcode
2. Select File → New → Target
3. Choose "iOS" → "App"
4. Name it "SubscriptionTrackerApp"
5. Add the UI views to the new target
6. The app will now appear in the iOS simulator as a standalone app

## Alternative: Create Xcode Project from Command Line

You can also generate an Xcode project file:

```bash
cd SubscriptionTrackerApp
swift package generate-xcodeproj
```

Then open `SubscriptionTracker.xcodeproj` in Xcode.

## Project Structure for iOS

```
SubscriptionTrackerApp/
├── Package.swift                           # Swift Package Manager manifest
├── Sources/
│   ├── SubscriptionTrackerCore/           # Core business logic (platform-independent)
│   │   ├── Subscription.swift             # Data model
│   │   └── SubscriptionManager.swift      # Manager for CRUD operations
│   └── SubscriptionTrackerUI/             # SwiftUI views (iOS/macOS only)
│       ├── ObservableSubscriptionManager.swift
│       ├── SubscriptionListView.swift     # Main list view
│       ├── AddEditSubscriptionView.swift  # Add/Edit form
│       └── SubscriptionTrackerApp.swift   # App entry point
└── Tests/
    └── SubscriptionTrackerTests/          # Unit tests
        ├── SubscriptionTests.swift
        └── SubscriptionManagerTests.swift
```

## Building on Different Platforms

### On macOS with Xcode
- Build everything: `swift build` (in Terminal) or use Xcode UI
- Run tests: `swift test` or press `Cmd+U` in Xcode
- Full SwiftUI app development is supported

### On Linux
- Build core logic only: `swift build --target SubscriptionTrackerCore`
- Run tests: `swift test`
- SwiftUI is not available on Linux, only the Core module can be built

## Troubleshooting

### "No such module 'SwiftUI'" error
This error occurs when trying to build SwiftUI code on Linux. Make sure you're only building the Core target:
```bash
swift build --target SubscriptionTrackerCore
```

### Code signing errors on device
Make sure you have:
1. A valid Apple Developer account
2. The correct provisioning profile
3. Your device added to your developer account

### Simulator not appearing
Make sure you have the iOS simulator installed:
1. Open Xcode
2. Go to Preferences → Components
3. Download the iOS simulator if needed

## Next Steps

Once you have the app running in Xcode:

1. Customize the UI colors and styling
2. Add app icons and launch screen
3. Implement notifications for subscription renewals
4. Add data export functionality
5. Implement iCloud sync
6. Create widgets for the home screen
7. Add localization for multiple languages

## Running Tests in Xcode

1. Open the project in Xcode
2. Press `Cmd+U` to run all tests
3. View test results in the Test Navigator (Cmd+6)
4. Individual tests can be run by clicking the diamond icon next to each test

## Continuous Integration

For CI/CD on non-macOS platforms, only the Core module tests will run:
```bash
swift test  # Will automatically skip UI module on Linux
```
