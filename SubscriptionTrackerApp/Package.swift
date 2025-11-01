// swift-tools-version:5.9
import PackageDescription

// Note: The SubscriptionTrackerUI module is intentionally not included in the package
// definition because it requires SwiftUI, which is only available on Apple platforms.
// When opened in Xcode on macOS, the UI module will be automatically available.
// For cross-platform builds (e.g., Linux CI), only the Core module is built.

let package = Package(
    name: "SubscriptionTracker",
    platforms: [
        .iOS(.v16),
        .macOS(.v13)
    ],
    products: [
        .library(
            name: "SubscriptionTrackerCore",
            targets: ["SubscriptionTrackerCore"]
        ),
    ],
    targets: [
        .target(
            name: "SubscriptionTrackerCore",
            dependencies: [],
            path: "Sources/SubscriptionTrackerCore"
        ),
        .testTarget(
            name: "SubscriptionTrackerTests",
            dependencies: ["SubscriptionTrackerCore"]
        ),
    ]
)
