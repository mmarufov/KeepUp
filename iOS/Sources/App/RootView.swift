import SwiftUI

struct RootView: View {
    var body: some View {
        FeedView(viewModel: FeedViewModel())
    }
}

struct RootView_Previews: PreviewProvider {
    static var previews: some View {
        RootView()
    }
}



