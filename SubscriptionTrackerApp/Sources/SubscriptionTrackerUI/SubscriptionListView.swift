import SwiftUI
import SubscriptionTrackerCore

/// Main view displaying the list of subscriptions
public struct SubscriptionListView: View {
    @StateObject private var manager = ObservableSubscriptionManager()
    @State private var showingAddSheet = false
    @State private var selectedSubscription: Subscription?
    
    public init() {}
    
    public var body: some View {
        NavigationView {
            VStack {
                // Summary Card
                summaryCard
                
                // Subscriptions List
                if manager.subscriptions.isEmpty {
                    emptyStateView
                } else {
                    subscriptionsList
                }
            }
            .navigationTitle("Subscriptions")
            .toolbar {
                ToolbarItem(placement: .navigationBarTrailing) {
                    Button(action: { showingAddSheet = true }) {
                        Image(systemName: "plus")
                    }
                }
            }
            .sheet(isPresented: $showingAddSheet) {
                AddEditSubscriptionView(manager: manager)
            }
            .sheet(item: $selectedSubscription) { subscription in
                AddEditSubscriptionView(manager: manager, subscription: subscription)
            }
        }
    }
    
    private var summaryCard: some View {
        VStack(alignment: .leading, spacing: 8) {
            HStack {
                VStack(alignment: .leading) {
                    Text("Monthly Total")
                        .font(.subheadline)
                        .foregroundColor(.secondary)
                    Text("$\(manager.totalMonthlyCost, specifier: "%.2f")")
                        .font(.title2)
                        .fontWeight(.bold)
                }
                Spacer()
                VStack(alignment: .trailing) {
                    Text("Yearly Total")
                        .font(.subheadline)
                        .foregroundColor(.secondary)
                    Text("$\(manager.totalYearlyCost, specifier: "%.2f")")
                        .font(.title2)
                        .fontWeight(.bold)
                }
            }
            Text("\(manager.activeSubscriptionsCount) active subscriptions")
                .font(.caption)
                .foregroundColor(.secondary)
        }
        .padding()
        .background(Color.blue.opacity(0.1))
        .cornerRadius(12)
        .padding()
    }
    
    private var emptyStateView: some View {
        VStack(spacing: 20) {
            Image(systemName: "creditcard")
                .font(.system(size: 60))
                .foregroundColor(.gray)
            Text("No subscriptions yet")
                .font(.title2)
                .fontWeight(.medium)
            Text("Tap the + button to add your first subscription")
                .font(.subheadline)
                .foregroundColor(.secondary)
                .multilineTextAlignment(.center)
        }
        .padding()
    }
    
    private var subscriptionsList: some View {
        List {
            ForEach(manager.subscriptions) { subscription in
                SubscriptionRowView(subscription: subscription)
                    .onTapGesture {
                        selectedSubscription = subscription
                    }
            }
            .onDelete(perform: manager.deleteSubscriptions)
        }
    }
}

/// Row view for displaying a single subscription
struct SubscriptionRowView: View {
    let subscription: Subscription
    
    var body: some View {
        HStack {
            VStack(alignment: .leading, spacing: 4) {
                Text(subscription.name)
                    .font(.headline)
                Text(subscription.category)
                    .font(.caption)
                    .foregroundColor(.secondary)
            }
            
            Spacer()
            
            VStack(alignment: .trailing, spacing: 4) {
                Text("$\(subscription.cost, specifier: "%.2f")")
                    .font(.headline)
                    .foregroundColor(subscription.isActive ? .primary : .secondary)
                Text(subscription.billingCycle.rawValue)
                    .font(.caption)
                    .foregroundColor(.secondary)
            }
        }
        .opacity(subscription.isActive ? 1.0 : 0.6)
    }
}

#if DEBUG
struct SubscriptionListView_Previews: PreviewProvider {
    static var previews: some View {
        SubscriptionListView()
    }
}
#endif
