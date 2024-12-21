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
  host: "http://localhost:9200",
  index: "cv-transcriptions",
});

// const CustomResultView = ({ result }) => {
//   return (
//     <div>
//       <h3>{result.generated_text ? result.generated_text.raw : "No generated text"}</h3>
//       <p>Duration: {result.duration ? result.duration.raw : "N/A"}</p>
//       <p>Age: {result.age ? result.age.raw : "Unknown"}</p>
//       <p>Gender: {result.gender ? result.gender.raw : "Unknown"}</p>
//       <p>Accent: {result.accent ? result.accent.raw : "Unknown"}</p>
//     </div>
//   );
// };


// const ResultsComponent = ({ results }) => {
//   console.log("Search Results: ", results);
//   return (
//     <div>
//       {results.length > 0 ? (
//         results.map((result, index) => (
//           <CustomResultView key={index} result={result} />
//         ))
//       ) : (
//         <p>No results found</p>
//       )}
//     </div>
//   );
// };


const config = {
  debug: true,
  alwaysSearchOnInitialLoad: true,
  apiConnector: connector,
  hasA11yNotifications: true,
  searchQuery: {
    search_fields: {
      text: {}, // Search on the 'text' field which contains actual transcription data
      generated_text: {}, // Optional: If you want to try searching on this field too, but it's often empty
      age: {},
      gender: {},
      accent: {},
    },
    result_fields: {
      text: { raw: {} },
      generated_text: { raw: {} },
      age: { raw: {} },
      gender: { raw: {} },
      accent: { raw: {} },
    },
  },
};


function App() {
  return (
    <SearchProvider config={config}>
      <div className="App">
        <SearchBox />
        {/* Ensure you use the resultView prop for custom result display */}
        <Results />
        <Paging />
      </div>
    </SearchProvider>
  );
}

export default App;
