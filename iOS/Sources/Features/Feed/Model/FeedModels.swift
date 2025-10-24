import Foundation

struct FeedItem: Identifiable, Equatable {
    let id: Int64
    let title: String
    let subtitle: String
    let imageURL: URL?
    let source: String
    let publishedAt: Date?
}


