import SwiftUI
import SubscriptionTrackerCore

/// Main app entry point for the Subscription Tracker
@main
public struct SubscriptionTrackerApp: App {
    public init() {}
    
    public var body: some Scene {
        WindowGroup {
            SubscriptionListView()
        }
    }
}
