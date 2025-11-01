import XCTest
@testable import SubscriptionTrackerTests

fileprivate extension SubscriptionManagerTests {
    @available(*, deprecated, message: "Not actually deprecated. Marked as deprecated to allow inclusion of deprecated tests (which test deprecated functionality) without warnings")
    static nonisolated(unsafe) let __allTests__SubscriptionManagerTests = [
        ("testActiveSubscriptionsCount", testActiveSubscriptionsCount),
        ("testAddSubscription", testAddSubscription),
        ("testClearAllSubscriptions", testClearAllSubscriptions),
        ("testDeleteSubscription", testDeleteSubscription),
        ("testGetSubscriptionById", testGetSubscriptionById),
        ("testPersistence", testPersistence),
        ("testSubscriptionsByCategory", testSubscriptionsByCategory),
        ("testTotalMonthlyCost", testTotalMonthlyCost),
        ("testTotalYearlyCost", testTotalYearlyCost),
        ("testUpdateSubscription", testUpdateSubscription)
    ]
}

fileprivate extension SubscriptionTests {
    @available(*, deprecated, message: "Not actually deprecated. Marked as deprecated to allow inclusion of deprecated tests (which test deprecated functionality) without warnings")
    static nonisolated(unsafe) let __allTests__SubscriptionTests = [
        ("testMonthlyCostCalculation", testMonthlyCostCalculation),
        ("testNextRenewalDate", testNextRenewalDate),
        ("testSubscriptionCodable", testSubscriptionCodable),
        ("testSubscriptionCreation", testSubscriptionCreation),
        ("testSubscriptionEquality", testSubscriptionEquality),
        ("testYearlyCostCalculation", testYearlyCostCalculation)
    ]
}
@available(*, deprecated, message: "Not actually deprecated. Marked as deprecated to allow inclusion of deprecated tests (which test deprecated functionality) without warnings")
func __SubscriptionTrackerTests__allTests() -> [XCTestCaseEntry] {
    return [
        testCase(SubscriptionManagerTests.__allTests__SubscriptionManagerTests),
        testCase(SubscriptionTests.__allTests__SubscriptionTests)
    ]
}