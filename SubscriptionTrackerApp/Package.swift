// swift-tools-version:5.9
import PackageDescription

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
