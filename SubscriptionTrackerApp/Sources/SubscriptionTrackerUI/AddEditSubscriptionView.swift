import SwiftUI
import SubscriptionTrackerCore

/// View for adding or editing a subscription
public struct AddEditSubscriptionView: View {
    @ObservedObject var manager: ObservableSubscriptionManager
    @Environment(\.dismiss) private var dismiss
    
    @State private var name: String
    @State private var cost: String
    @State private var billingCycle: BillingCycle
    @State private var renewalDate: Date
    @State private var category: String
    @State private var isActive: Bool
    
    private let subscription: Subscription?
    private let isEditMode: Bool
    
    public init(manager: ObservableSubscriptionManager, subscription: Subscription? = nil) {
        self.manager = manager
        self.subscription = subscription
        self.isEditMode = subscription != nil
        
        _name = State(initialValue: subscription?.name ?? "")
        _cost = State(initialValue: subscription != nil ? String(format: "%.2f", subscription!.cost) : "")
        _billingCycle = State(initialValue: subscription?.billingCycle ?? .monthly)
        _renewalDate = State(initialValue: subscription?.renewalDate ?? Date())
        _category = State(initialValue: subscription?.category ?? "General")
        _isActive = State(initialValue: subscription?.isActive ?? true)
    }
    
    public var body: some View {
        NavigationView {
            Form {
                Section(header: Text("Subscription Details")) {
                    TextField("Name", text: $name)
                    TextField("Cost", text: $cost)
                        .keyboardType(.decimalPad)
                    Picker("Billing Cycle", selection: $billingCycle) {
                        ForEach(BillingCycle.allCases, id: \.self) { cycle in
                            Text(cycle.rawValue).tag(cycle)
                        }
                    }
                }
                
                Section(header: Text("Additional Information")) {
                    DatePicker("Renewal Date", selection: $renewalDate, displayedComponents: .date)
                    TextField("Category", text: $category)
                    Toggle("Active", isOn: $isActive)
                }
                
                if isEditMode {
                    Section(header: Text("Cost Analysis")) {
                        if let sub = subscription {
                            HStack {
                                Text("Monthly Cost")
                                Spacer()
                                Text("$\(sub.monthlyCost, specifier: "%.2f")")
                            }
                            HStack {
                                Text("Yearly Cost")
                                Spacer()
                                Text("$\(sub.yearlyCost, specifier: "%.2f")")
                            }
                            HStack {
                                Text("Next Renewal")
                                Spacer()
                                Text(sub.nextRenewalDate(), style: .date)
                            }
                        }
                    }
                }
            }
            .navigationTitle(isEditMode ? "Edit Subscription" : "Add Subscription")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .navigationBarLeading) {
                    Button("Cancel") {
                        dismiss()
                    }
                }
                ToolbarItem(placement: .navigationBarTrailing) {
                    Button("Save") {
                        saveSubscription()
                    }
                    .disabled(!isFormValid)
                }
            }
        }
    }
    
    private var isFormValid: Bool {
        guard !name.isEmpty,
              let costValue = Double(cost),
              costValue > 0 else {
            return false
        }
        return true
    }
    
    private func saveSubscription() {
        guard let costValue = Double(cost), costValue > 0 else { return }
        
        if let existingSubscription = subscription {
            // Update existing subscription
            let updated = Subscription(
                id: existingSubscription.id,
                name: name,
                cost: costValue,
                billingCycle: billingCycle,
                renewalDate: renewalDate,
                category: category,
                isActive: isActive
            )
            manager.updateSubscription(updated)
        } else {
            // Create new subscription
            let new = Subscription(
                name: name,
                cost: costValue,
                billingCycle: billingCycle,
                renewalDate: renewalDate,
                category: category,
                isActive: isActive
            )
            manager.addSubscription(new)
        }
        
        dismiss()
    }
}

#if DEBUG
struct AddEditSubscriptionView_Previews: PreviewProvider {
    static var previews: some View {
        AddEditSubscriptionView(manager: ObservableSubscriptionManager())
    }
}
#endif
