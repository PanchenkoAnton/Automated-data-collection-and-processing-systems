import Foundation

/// Represents the billing cycle for a subscription
public enum BillingCycle: String, Codable, CaseIterable {
    case weekly = "Weekly"
    case monthly = "Monthly"
    case quarterly = "Quarterly"
    case yearly = "Yearly"
    
    /// Average weeks per month (52 weeks / 12 months)
    private static let averageWeeksPerMonth: Double = 4.33
    
    /// Returns the approximate number of days in the billing cycle
    /// Note: Monthly is approximated as 30 days for simplicity
    public var days: Int {
        switch self {
        case .weekly: return 7
        case .monthly: return 30
        case .quarterly: return 90
        case .yearly: return 365
        }
    }
    
    /// Converts the cost to monthly equivalent
    func toMonthlyCost(_ cost: Double) -> Double {
        switch self {
        case .weekly: return cost * Self.averageWeeksPerMonth
        case .monthly: return cost
        case .quarterly: return cost / 3
        case .yearly: return cost / 12
        }
    }
    
    /// Converts the cost to yearly equivalent
    func toYearlyCost(_ cost: Double) -> Double {
        switch self {
        case .weekly: return cost * 52
        case .monthly: return cost * 12
        case .quarterly: return cost * 4
        case .yearly: return cost
        }
    }
}

/// Represents a subscription with all necessary information
public struct Subscription: Identifiable, Codable, Equatable {
    public let id: UUID
    public var name: String
    public var cost: Double
    public var billingCycle: BillingCycle
    public var renewalDate: Date
    public var category: String
    public var isActive: Bool
    
    public init(
        id: UUID = UUID(),
        name: String,
        cost: Double,
        billingCycle: BillingCycle,
        renewalDate: Date,
        category: String = "General",
        isActive: Bool = true
    ) {
        self.id = id
        self.name = name
        self.cost = cost
        self.billingCycle = billingCycle
        self.renewalDate = renewalDate
        self.category = category
        self.isActive = isActive
    }
    
    /// Calculate the next renewal date based on billing cycle
    public func nextRenewalDate() -> Date {
        Calendar.current.date(byAdding: .day, value: billingCycle.days, to: renewalDate) ?? renewalDate
    }
    
    /// Calculate monthly cost regardless of billing cycle
    public var monthlyCost: Double {
        billingCycle.toMonthlyCost(cost)
    }
    
    /// Calculate yearly cost
    public var yearlyCost: Double {
        billingCycle.toYearlyCost(cost)
    }
}
