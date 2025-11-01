# Subscription Tracker iOS App

A modern iOS application for tracking and managing your subscriptions, built with SwiftUI.

## Features

### Core Functionality
- **Add/Edit/Delete Subscriptions**: Manage your subscriptions with ease
- **Multiple Billing Cycles**: Support for weekly, monthly, quarterly, and yearly billing
- **Cost Analytics**: 
  - Calculate monthly and yearly costs for each subscription
  - View total monthly and yearly spending across all subscriptions
  - Track active subscriptions count
- **Category Organization**: Organize subscriptions by custom categories
- **Renewal Date Tracking**: Keep track of when each subscription renews
- **Active/Inactive Status**: Mark subscriptions as active or inactive
- **Data Persistence**: All data is saved locally using UserDefaults

### User Interface
- Clean, modern SwiftUI interface
- Summary dashboard showing total costs
- Easy-to-use forms for adding and editing subscriptions
- Swipe-to-delete functionality
- Empty state guidance for new users

## Architecture

### Components

#### Models
- **`Subscription`**: Core data model representing a subscription
  - Properties: name, cost, billing cycle, renewal date, category, active status
  - Methods: Calculate next renewal date, monthly cost, yearly cost

- **`BillingCycle`**: Enum for different billing cycles
  - Cases: weekly, monthly, quarterly, yearly
  - Provides day count for each cycle

#### Managers
- **`SubscriptionManager`**: Handles CRUD operations and persistence
  - Add, update, delete subscriptions
  - Calculate total costs
  - Group subscriptions by category
  - Save/load from UserDefaults

#### Views
- **`SubscriptionListView`**: Main view displaying all subscriptions
  - Summary card with total costs
  - List of subscriptions
  - Navigation to add/edit views

- **`AddEditSubscriptionView`**: Form for creating or editing subscriptions
  - Input fields for all subscription properties
  - Cost analysis for existing subscriptions
  - Form validation

- **`SubscriptionTrackerApp`**: Main app entry point

## Requirements

- iOS 16.0+
- Swift 5.9+
- Xcode 15.0+

## Building the Project

### Using Swift Package Manager

```bash
cd SubscriptionTrackerApp
swift build
```

### Running Tests

```bash
swift test
```

### Opening in Xcode

1. Open `Package.swift` in Xcode
2. Select your target device or simulator
3. Press Cmd+R to build and run

## Project Structure

```
SubscriptionTrackerApp/
├── Package.swift
├── Sources/
│   ├── SubscriptionTrackerCore/           # Core business logic (platform-independent)
│   │   ├── Subscription.swift             # Data model
│   │   └── SubscriptionManager.swift      # Business logic & persistence
│   └── SubscriptionTrackerUI/             # SwiftUI views (iOS/macOS only)
│       ├── ObservableSubscriptionManager.swift
│       ├── SubscriptionListView.swift     # Main list view
│       ├── AddEditSubscriptionView.swift  # Add/Edit form
│       └── SubscriptionTrackerApp.swift   # App entry point
└── Tests/
    └── SubscriptionTrackerTests/
        ├── SubscriptionTests.swift         # Model tests
        └── SubscriptionManagerTests.swift  # Manager tests
```

## Usage Examples

### Adding a Subscription

```swift
let manager = SubscriptionManager()

let subscription = Subscription(
    name: "Netflix",
    cost: 15.99,
    billingCycle: .monthly,
    renewalDate: Date(),
    category: "Entertainment"
)

manager.addSubscription(subscription)
```

### Calculating Total Costs

```swift
let monthlyTotal = manager.totalMonthlyCost
let yearlyTotal = manager.totalYearlyCost
```

### Filtering by Category

```swift
let grouped = manager.subscriptionsByCategory
let entertainmentSubs = grouped["Entertainment"]
```

## Testing

The project includes comprehensive unit tests covering:
- Subscription model creation and calculations
- Cost calculations for different billing cycles
- CRUD operations in the manager
- Data persistence
- Category grouping
- Active/inactive filtering

Run tests with: `swift test`

## Data Persistence

Subscriptions are automatically saved to UserDefaults whenever they are added, updated, or deleted. The data persists across app launches.

## Future Enhancements

Potential features for future releases:
- Notifications for upcoming renewals
- Export data to CSV
- Charts and visualizations
- Multiple currency support
- iCloud sync
- Widget support
- Dark mode optimization

## License

This project is part of the "Automated data collection and processing systems" university course at SPBU.

## Contributors

- Ermolaev Aleksey
- Panchenko Anton
