import SwiftUI

struct FeedView: View {
    @StateObject var viewModel: FeedViewModel

    var body: some View {
        NavigationView {
            List(viewModel.items) { item in
                HStack(alignment: .top, spacing: 12) {
                    if let url = item.imageURL {
                        AsyncImage(url: url) { image in
                            image.resizable().scaledToFill()
                        } placeholder: {
                            Color.gray.opacity(0.2)
                        }
                        .frame(width: 80, height: 80)
                        .clipped()
                        .cornerRadius(8)
                    }
                    VStack(alignment: .leading, spacing: 6) {
                        Text(item.title).font(.headline).lineLimit(2)
                        if !item.subtitle.isEmpty { Text(item.subtitle).font(.subheadline).foregroundColor(.secondary).lineLimit(2) }
                        Text(item.source).font(.caption).foregroundColor(.secondary)
                    }
                }
                .padding(.vertical, 4)
            }
            .overlay {
                if viewModel.isLoading { ProgressView() }
            }
            .navigationTitle("KeepUp")
            .task { viewModel.load() }
            .refreshable { await viewModel.refresh() }
        }
    }
}

struct FeedView_Previews: PreviewProvider {
    static var previews: some View {
        FeedView(viewModel: FeedViewModel())
    }
}



