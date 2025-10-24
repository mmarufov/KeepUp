import Foundation
import Supabase

final class SupabaseService {
    static let shared = SupabaseService()

    private let client: SupabaseClient

    private init() {
        let url = Bundle.main.object(forInfoDictionaryKey: "SUPABASE_URL") as? String ?? ""
        let anon = Bundle.main.object(forInfoDictionaryKey: "SUPABASE_ANON_KEY") as? String ?? ""
        self.client = SupabaseClient(supabaseURL: URL(string: url)!, supabaseKey: anon)
    }

    struct Article: Decodable, Identifiable {
        let id: Int64
        let title: String?
        let description: String?
        let image_url: String?
        let source: String?
        let published_at: String?
        let lang: String?
    }

    func getLatestArticles(limit: Int = 20, before: Date? = nil) async throws -> [Article] {
        struct RPCLatest: Decodable { let id: Int64; let title: String?; let description: String?; let image_url: String?; let source: String?; let published_at: String?; let lang: String? }
        var params: [String: AnyEncodable] = ["p_limit": AnyEncodable(limit)]
        if let before = before { params["p_before"] = AnyEncodable(ISO8601DateFormatter().string(from: before)) }
        let res: [RPCLatest] = try await client.functions.invoke("get_latest_articles", options: FunctionInvokeOptions(
            method: .post,
            body: params
        ))
        return res.map { Article(id: $0.id, title: $0.title, description: $0.description, image_url: $0.image_url, source: $0.source, published_at: $0.published_at, lang: $0.lang) }
    }
}



