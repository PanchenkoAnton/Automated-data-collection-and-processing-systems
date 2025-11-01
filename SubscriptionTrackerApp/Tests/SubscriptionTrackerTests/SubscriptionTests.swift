import XCTest
@testable import SubscriptionTrackerCore

final class SubscriptionTests: XCTestCase {
    
    func testSubscriptionCreation() {
        let subscription = Subscription(
            name: "Netflix",
            cost: 15.99,
            billingCycle: .monthly,
            renewalDate: Date(),
            category: "Entertainment"
        )
        
        XCTAssertEqual(subscription.name, "Netflix")
        XCTAssertEqual(subscription.cost, 15.99)
        XCTAssertEqual(subscription.billingCycle, .monthly)
        XCTAssertEqual(subscription.category, "Entertainment")
        XCTAssertTrue(subscription.isActive)
    }
    
    func testMonthlyCostCalculation() {
        let weekly = Subscription(name: "Test", cost: 5.0, billingCycle: .weekly, renewalDate: Date())
        let monthly = Subscription(name: "Test", cost: 10.0, billingCycle: .monthly, renewalDate: Date())
        let quarterly = Subscription(name: "Test", cost: 30.0, billingCycle: .quarterly, renewalDate: Date())
        let yearly = Subscription(name: "Test", cost: 120.0, billingCycle: .yearly, renewalDate: Date())
        
        XCTAssertEqual(weekly.monthlyCost, 21.65, accuracy: 0.01)
        XCTAssertEqual(monthly.monthlyCost, 10.0)
        XCTAssertEqual(quarterly.monthlyCost, 10.0)
        XCTAssertEqual(yearly.monthlyCost, 10.0)
    }
    
    func testYearlyCostCalculation() {
        let weekly = Subscription(name: "Test", cost: 5.0, billingCycle: .weekly, renewalDate: Date())
        let monthly = Subscription(name: "Test", cost: 10.0, billingCycle: .monthly, renewalDate: Date())
        let quarterly = Subscription(name: "Test", cost: 30.0, billingCycle: .quarterly, renewalDate: Date())
        let yearly = Subscription(name: "Test", cost: 120.0, billingCycle: .yearly, renewalDate: Date())
        
        XCTAssertEqual(weekly.yearlyCost, 260.0)
        XCTAssertEqual(monthly.yearlyCost, 120.0)
        XCTAssertEqual(quarterly.yearlyCost, 120.0)
        XCTAssertEqual(yearly.yearlyCost, 120.0)
    }
    
    func testNextRenewalDate() {
        let startDate = Date()
        let subscription = Subscription(
            name: "Test",
            cost: 10.0,
            billingCycle: .monthly,
            renewalDate: startDate
        )
        
        let nextDate = subscription.nextRenewalDate()
        let calendar = Calendar.current
        let difference = calendar.dateComponents([.day], from: startDate, to: nextDate)
        
        XCTAssertEqual(difference.day, 30)
    }
    
    func testSubscriptionEquality() {
        let id = UUID()
        let date = Date()
        let sub1 = Subscription(id: id, name: "Test", cost: 10.0, billingCycle: .monthly, renewalDate: date)
        let sub2 = Subscription(id: id, name: "Test", cost: 10.0, billingCycle: .monthly, renewalDate: date)
        
        XCTAssertEqual(sub1.id, sub2.id)
        XCTAssertEqual(sub1.name, sub2.name)
        XCTAssertEqual(sub1.cost, sub2.cost)
        XCTAssertEqual(sub1.billingCycle, sub2.billingCycle)
    }
    
    func testSubscriptionCodable() throws {
        let date = Date()
        let subscription = Subscription(
            name: "Netflix",
            cost: 15.99,
            billingCycle: .monthly,
            renewalDate: date,
            category: "Entertainment"
        )
        
        let encoder = JSONEncoder()
        encoder.dateEncodingStrategy = .iso8601
        let data = try encoder.encode(subscription)
        
        let decoder = JSONDecoder()
        decoder.dateDecodingStrategy = .iso8601
        let decoded = try decoder.decode(Subscription.self, from: data)
        
        XCTAssertEqual(subscription.id, decoded.id)
        XCTAssertEqual(subscription.name, decoded.name)
        XCTAssertEqual(subscription.cost, decoded.cost)
        XCTAssertEqual(subscription.billingCycle, decoded.billingCycle)
        XCTAssertEqual(subscription.category, decoded.category)
        XCTAssertEqual(subscription.isActive, decoded.isActive)
    }
}
