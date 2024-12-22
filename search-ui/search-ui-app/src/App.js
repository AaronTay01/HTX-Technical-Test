import React from "react";
import {
  SearchProvider,
  SearchBox,
  Results,
  Paging,
} from "@elastic/react-search-ui";
import ElasticsearchConnector from '@elastic/search-ui-elasticsearch-connector';
import "@elastic/react-search-ui-views/lib/styles/styles.css";

const connector = new ElasticsearchConnector({
  connectionOptions: {
    nodes: [
      "http://elasticsearch-node1:9200",  // Node 1
      "http://elasticsearch-node2:9201",  // Node 2
    ],
    // You may also need to add authentication here if your cluster requires it.
  },
  host: "http://localhost:9200",  // Primary host
  index: "cv-transcriptions",
});

// const CustomResultView = ({ result }) => {
//   return (
//     <div>
//       <h3>{result.generated_text ? result.generated_text.raw : "No generated text"}</h3>
//       <p>Duration: {result.duration && result.duration.raw ? result.duration.raw : "N/A"}</p>
//       <p>Age: {result.age && result.age.raw !== -1 ? result.age.raw : "Unknown"}</p>
//       <p>Gender: {result.gender && result.gender.raw ? result.gender.raw : "Unknown"}</p>
//       <p>Accent: {result.accent && result.accent.raw ? result.accent.raw : "Unknown"}</p>
//     </div>
//   );
// };

const config = {
  debug: true,
  alwaysSearchOnInitialLoad: true,
  apiConnector: connector,
  hasA11yNotifications: true,
  searchQuery: {
    query: {
      match: {
        text: {}
      }
    },
    result_fields: {
      text: { raw: {} },
      generated_text: { raw: {} },
      age: { raw: {} },
      gender: { raw: {} },
      accent: { raw: {} }
    },
  },
  
};

function App() {
  return (
    <SearchProvider config={config}>
      <div className="App">
        <SearchBox />
        <Results />
        <Paging />
      </div>
    </SearchProvider>
  );
}

export default App;
