import Foundation

@MainActor
final class FeedViewModel: ObservableObject {
    @Published var items: [FeedItem] = []
    @Published var isLoading: Bool = false
    @Published var errorMessage: String?

    func load() {
        Task { await refresh() }
    }

    func refresh() async {
        isLoading = true
        defer { isLoading = false }
        do {
            let articles = try await SupabaseService.shared.getLatestArticles(limit: 20)
            items = articles.map { a in
                FeedItem(
                    id: a.id,
                    title: a.title ?? "",
                    subtitle: a.description ?? "",
                    imageURL: (a.image_url.flatMap { URL(string: $0) }),
                    source: a.source ?? "",
                    publishedAt: a.published_at.flatMap { ISO8601DateFormatter().date(from: $0) }
                )
            }
        } catch {
            errorMessage = error.localizedDescription
        }
    }
}


