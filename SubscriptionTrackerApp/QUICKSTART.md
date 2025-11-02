# Quick Start Guide

Get up and running with the Subscription Tracker iOS app in minutes!

## For iOS Development (macOS with Xcode)

### Prerequisites
- macOS 13.0 or later
- Xcode 15.0 or later
- An Apple Developer account (for device deployment)

### Setup Steps

1. **Open the project in Xcode:**
   ```bash
   cd SubscriptionTrackerApp
   open Package.swift
   ```
   
2. **Wait for dependencies to resolve** (automatic in Xcode)

3. **Select a simulator:**
   - Click the device dropdown at the top
   - Choose "iPhone 15 Pro" or your preferred simulator

4. **Build and run:**
   - Press `Cmd + R` or click the Play button
   - The app will launch in the simulator

### First Time Use

1. **Add your first subscription:**
   - Tap the "+" button in the top-right corner
   - Fill in the subscription details:
     - Name: e.g., "Netflix"
     - Cost: e.g., "15.99"
     - Billing Cycle: Choose from Weekly/Monthly/Quarterly/Yearly
     - Renewal Date: Select the next billing date
     - Category: e.g., "Entertainment"
   - Tap "Save"

2. **View your subscriptions:**
   - See all subscriptions in the main list
   - Total monthly and yearly costs appear at the top
   - Tap any subscription to edit it

3. **Delete a subscription:**
   - Swipe left on any subscription
   - Tap "Delete"

## For Testing (Any Platform with Swift)

### Prerequisites
- Swift 5.9 or later

### Run Tests

```bash
cd SubscriptionTrackerApp
swift test
```

Expected output:
```
Test Suite 'All tests' passed
Executed 16 tests, with 0 failures
```

## For Development

### Project Structure
```
Sources/
├── SubscriptionTrackerCore/    # Business logic (edit here for features)
└── SubscriptionTrackerUI/       # UI views (edit here for interface)

Tests/
└── SubscriptionTrackerTests/   # Add your tests here
```

### Making Changes

1. **Add a new feature to the data model:**
   - Edit `Sources/SubscriptionTrackerCore/Subscription.swift`
   - Add tests in `Tests/SubscriptionTrackerTests/SubscriptionTests.swift`

2. **Add business logic:**
   - Edit `Sources/SubscriptionTrackerCore/SubscriptionManager.swift`
   - Add tests in `Tests/SubscriptionTrackerTests/SubscriptionManagerTests.swift`

3. **Customize the UI:**
   - Edit views in `Sources/SubscriptionTrackerUI/`
   - Run in Xcode to see changes immediately

### Running the App

**In Xcode:**
- Press `Cmd + R` to build and run
- Press `Cmd + U` to run tests
- Press `Cmd + B` to build only

**From Terminal:**
```bash
# Build the core logic
swift build --target SubscriptionTrackerCore

# Run all tests
swift test

# Clean build artifacts
rm -rf .build
```

## Common Tasks

### Add a new subscription programmatically
```swift
let manager = SubscriptionManager()
let subscription = Subscription(
    name: "Spotify",
    cost: 9.99,
    billingCycle: .monthly,
    renewalDate: Date(),
    category: "Music"
)
manager.addSubscription(subscription)
```

### Calculate total costs
```swift
let manager = SubscriptionManager()
print("Monthly: $\(manager.totalMonthlyCost)")
print("Yearly: $\(manager.totalYearlyCost)")
```

### Filter by category
```swift
let manager = SubscriptionManager()
let byCategory = manager.subscriptionsByCategory
let entertainment = byCategory["Entertainment"] ?? []
print("Entertainment subscriptions: \(entertainment.count)")
```

## Troubleshooting

### "No such module 'SwiftUI'" error
- **Cause:** Trying to build UI code on Linux
- **Solution:** Build only the Core module: `swift build --target SubscriptionTrackerCore`

### App won't run on device
- **Cause:** Code signing not configured
- **Solution:** 
  1. Open project in Xcode
  2. Select project → Signing & Capabilities
  3. Choose your Team
  4. Connect device and run

### Tests fail
- **Cause:** Leftover test data
- **Solution:** Tests use isolated UserDefaults, should not persist

### Build is slow
- **Cause:** First build downloads dependencies
- **Solution:** Subsequent builds will be faster

## Next Steps

Once you're comfortable with the basics:

1. **Read the full README:** `README.md` for comprehensive documentation
2. **Check the Xcode Guide:** `XCODE_GUIDE.md` for iOS-specific tips
3. **Review the implementation:** `IMPLEMENTATION_SUMMARY.md` for architecture details
4. **Customize the app:** Add your own features and styling
5. **Deploy to device:** Test on a real iOS device

## Resources

- **Apple Developer:** https://developer.apple.com
- **Swift Documentation:** https://swift.org/documentation/
- **SwiftUI Tutorials:** https://developer.apple.com/tutorials/swiftui

## Need Help?

- Check the documentation in the `SubscriptionTrackerApp` folder
- Review the test files for usage examples
- Examine the source code comments for implementation details

Happy tracking! 🎉
