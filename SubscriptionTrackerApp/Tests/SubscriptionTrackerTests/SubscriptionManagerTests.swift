import XCTest
@testable import SubscriptionTrackerCore

final class SubscriptionManagerTests: XCTestCase {
    var manager: SubscriptionManager!
    var userDefaults: UserDefaults!
    
    override func setUp() {
        super.setUp()
        // Use a separate UserDefaults suite for testing
        userDefaults = UserDefaults(suiteName: "test-suite")
        userDefaults.removePersistentDomain(forName: "test-suite")
        manager = SubscriptionManager(userDefaults: userDefaults)
    }
    
    override func tearDown() {
        manager.clearAllSubscriptions()
        userDefaults.removePersistentDomain(forName: "test-suite")
        manager = nil
        userDefaults = nil
        super.tearDown()
    }
    
    func testAddSubscription() {
        let subscription = Subscription(
            name: "Spotify",
            cost: 9.99,
            billingCycle: .monthly,
            renewalDate: Date()
        )
        
        manager.addSubscription(subscription)
        
        XCTAssertEqual(manager.subscriptions.count, 1)
        XCTAssertEqual(manager.subscriptions.first?.name, "Spotify")
    }
    
    func testUpdateSubscription() {
        var subscription = Subscription(
            name: "Netflix",
            cost: 15.99,
            billingCycle: .monthly,
            renewalDate: Date()
        )
        
        manager.addSubscription(subscription)
        
        subscription.cost = 19.99
        manager.updateSubscription(subscription)
        
        XCTAssertEqual(manager.subscriptions.first?.cost, 19.99)
    }
    
    func testDeleteSubscription() {
        let subscription = Subscription(
            name: "Hulu",
            cost: 7.99,
            billingCycle: .monthly,
            renewalDate: Date()
        )
        
        manager.addSubscription(subscription)
        XCTAssertEqual(manager.subscriptions.count, 1)
        
        manager.deleteSubscription(subscription)
        XCTAssertEqual(manager.subscriptions.count, 0)
    }
    
    func testGetSubscriptionById() {
        let subscription = Subscription(
            name: "Disney+",
            cost: 7.99,
            billingCycle: .monthly,
            renewalDate: Date()
        )
        
        manager.addSubscription(subscription)
        
        let retrieved = manager.getSubscription(byId: subscription.id)
        XCTAssertNotNil(retrieved)
        XCTAssertEqual(retrieved?.name, "Disney+")
    }
    
    func testTotalMonthlyCost() {
        let sub1 = Subscription(name: "Test1", cost: 10.0, billingCycle: .monthly, renewalDate: Date())
        let sub2 = Subscription(name: "Test2", cost: 15.0, billingCycle: .monthly, renewalDate: Date())
        let sub3 = Subscription(name: "Test3", cost: 5.0, billingCycle: .monthly, renewalDate: Date(), isActive: false)
        
        manager.addSubscription(sub1)
        manager.addSubscription(sub2)
        manager.addSubscription(sub3)
        
        XCTAssertEqual(manager.totalMonthlyCost, 25.0)
    }
    
    func testTotalYearlyCost() {
        let sub1 = Subscription(name: "Test1", cost: 10.0, billingCycle: .monthly, renewalDate: Date())
        let sub2 = Subscription(name: "Test2", cost: 120.0, billingCycle: .yearly, renewalDate: Date())
        
        manager.addSubscription(sub1)
        manager.addSubscription(sub2)
        
        XCTAssertEqual(manager.totalYearlyCost, 240.0)
    }
    
    func testActiveSubscriptionsCount() {
        let sub1 = Subscription(name: "Test1", cost: 10.0, billingCycle: .monthly, renewalDate: Date(), isActive: true)
        let sub2 = Subscription(name: "Test2", cost: 15.0, billingCycle: .monthly, renewalDate: Date(), isActive: true)
        let sub3 = Subscription(name: "Test3", cost: 5.0, billingCycle: .monthly, renewalDate: Date(), isActive: false)
        
        manager.addSubscription(sub1)
        manager.addSubscription(sub2)
        manager.addSubscription(sub3)
        
        XCTAssertEqual(manager.activeSubscriptionsCount, 2)
    }
    
    func testSubscriptionsByCategory() {
        let sub1 = Subscription(name: "Netflix", cost: 15.99, billingCycle: .monthly, renewalDate: Date(), category: "Entertainment")
        let sub2 = Subscription(name: "Spotify", cost: 9.99, billingCycle: .monthly, renewalDate: Date(), category: "Music")
        let sub3 = Subscription(name: "Hulu", cost: 7.99, billingCycle: .monthly, renewalDate: Date(), category: "Entertainment")
        
        manager.addSubscription(sub1)
        manager.addSubscription(sub2)
        manager.addSubscription(sub3)
        
        let grouped = manager.subscriptionsByCategory
        XCTAssertEqual(grouped["Entertainment"]?.count, 2)
        XCTAssertEqual(grouped["Music"]?.count, 1)
    }
    
    func testPersistence() {
        let subscription = Subscription(
            name: "Test Subscription",
            cost: 12.99,
            billingCycle: .monthly,
            renewalDate: Date()
        )
        
        manager.addSubscription(subscription)
        
        // Create a new manager with the same UserDefaults
        let newManager = SubscriptionManager(userDefaults: userDefaults)
        
        XCTAssertEqual(newManager.subscriptions.count, 1)
        XCTAssertEqual(newManager.subscriptions.first?.name, "Test Subscription")
    }
    
    func testClearAllSubscriptions() {
        let sub1 = Subscription(name: "Test1", cost: 10.0, billingCycle: .monthly, renewalDate: Date())
        let sub2 = Subscription(name: "Test2", cost: 15.0, billingCycle: .monthly, renewalDate: Date())
        
        manager.addSubscription(sub1)
        manager.addSubscription(sub2)
        
        XCTAssertEqual(manager.subscriptions.count, 2)
        
        manager.clearAllSubscriptions()
        
        XCTAssertEqual(manager.subscriptions.count, 0)
    }
}
