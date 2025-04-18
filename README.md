
# React App Test - Evidence-Based Policy (EBP) Evaluation Tool

First cut of using React to understand evidence-based policy making. The tool takes policy documents (briefs, regulations, testimony, etc.) and evaluates whether the policy has been rigorously evaluated (e.g., evidence-based). The `model` folder contains a functional, automated, scalable scoring tool for evaluating the evidence basis of real-world policy docs using LLMs. The `src` folder contains the source code for the React.app files. The `public` folder contains files instantiated with general React templates. Testing on more documents and using other models beyond Llama-b3 and Minstral are planned. 

### General File Structure:

    .
    ├── data
        ├── crs-bulk-pull.py    # Scrape 20k+ CRS reports, convert to .txt
        ├── crs-meta-merge.py   # For merging in CRS metadata
        ├── reports.csv         # CRS metadata file
    ├── model
        ├── txt                 # Sample of .txt CRS reports
        ├── validaton           # Validating model results
            ├── evidence_scores.csv
        ├── ebp-scoring-GPu.ipynb   # Colab GPU version of scoring model using LLM
        ├── ebp-scoring.ipynb   # CPU (local) version of scoring model using LLM
    ├── public
        ├── favicon.ico
        ├── index.html
        ├── logo192.png 
        ├── logo512.png
        ├── manifest.json
        ├── robots.txt    
    ├── src
        ├── App.css
        ├── App.js              # Primary app files
        ├── App.test.js
        ├── ProfileCard.css     # Add CSS if necessary
        ├── index.css
        ├── index.js
        ├── reportWebVitals.js
        ├── setupTests.js                 
    ├── package-lock.json                  
    ├── package.json                 
    └── README.md


# Why Evidence-Based Policymaking Scoring
This project helps answer a key question in policy evaluation: How evidence-based are the documents that inform or justify public policy? While many policies cite research or reference evaluations, there are few scalable ways to assess whether those references actually reflect evidence-based practices. This project offers a new, automated approach to do this.

I created a conceptual framework that defines what "evidence-based” means in concrete terms. It includes 5 core dimensions:

1. Use of empirical research
2. Structured evidence-gathering
3. Transparency of sources and methods
4. Expert or stakeholder consultation
5. Plans for evaluation or feedback

Each policy document is scored from 0 to 3 in each dimension, where 0 means that the feature is absent and 3 means it is strongly present.

### LLMs to Evaluate Policy Documents
Rather than reading and scoring documents manually, I use a large language model (LLM), which is a type of AI that understands and interprets text, to do the first round of evaluation. The LLM reads each document and applies the scoring rubric as if it were a policy analyst, returning both a score and a short explanation for each category.

This saves time, allows for rapid scaling across hundreds of documents, and offers consistent results based on the rubric I designed. Although it is not a replacement for expert review, it acts as an early warning system or classification tool to identify policies that may lack evidence.

> This is a minimum viable product currently in iteration. All of the boilerplate React information follows below.

## Getting Started with Create React App

This project was bootstrapped with [Create React App](https://github.com/facebook/create-react-app).

## Available Scripts

In the project directory, you can run:

### `npm start`

Runs the app in the development mode.\
Open [http://localhost:3000](http://localhost:3000) to view it in your browser.

The page will reload when you make changes.\
You may also see any lint errors in the console.

### `npm test`

Launches the test runner in the interactive watch mode.\
See the section about [running tests](https://facebook.github.io/create-react-app/docs/running-tests) for more information.

### `npm run build`

Builds the app for production to the `build` folder.\
It correctly bundles React in production mode and optimizes the build for the best performance.

The build is minified and the filenames include the hashes.\
Your app is ready to be deployed!

See the section about [deployment](https://facebook.github.io/create-react-app/docs/deployment) for more information.

### `npm run eject`

**Note: this is a one-way operation. Once you `eject`, you can't go back!**

If you aren't satisfied with the build tool and configuration choices, you can `eject` at any time. This command will remove the single build dependency from your project.

Instead, it will copy all the configuration files and the transitive dependencies (webpack, Babel, ESLint, etc) right into your project so you have full control over them. All of the commands except `eject` will still work, but they will point to the copied scripts so you can tweak them. At this point you're on your own.

You don't have to ever use `eject`. The curated feature set is suitable for small and middle deployments, and you shouldn't feel obligated to use this feature. However we understand that this tool wouldn't be useful if you couldn't customize it when you are ready for it.

## Learn More

You can learn more in the [Create React App documentation](https://facebook.github.io/create-react-app/docs/getting-started).

To learn React, check out the [React documentation](https://reactjs.org/).

### Code Splitting

This section has moved here: [https://facebook.github.io/create-react-app/docs/code-splitting](https://facebook.github.io/create-react-app/docs/code-splitting)

### Analyzing the Bundle Size

This section has moved here: [https://facebook.github.io/create-react-app/docs/analyzing-the-bundle-size](https://facebook.github.io/create-react-app/docs/analyzing-the-bundle-size)

### Making a Progressive Web App

This section has moved here: [https://facebook.github.io/create-react-app/docs/making-a-progressive-web-app](https://facebook.github.io/create-react-app/docs/making-a-progressive-web-app)

### Advanced Configuration

This section has moved here: [https://facebook.github.io/create-react-app/docs/advanced-configuration](https://facebook.github.io/create-react-app/docs/advanced-configuration)

### Deployment

This section has moved here: [https://facebook.github.io/create-react-app/docs/deployment](https://facebook.github.io/create-react-app/docs/deployment)

### `npm run build` fails to minify

This section has moved here: [https://facebook.github.io/create-react-app/docs/troubleshooting#npm-run-build-fails-to-minify](https://facebook.github.io/create-react-app/docs/troubleshooting#npm-run-build-fails-to-minify)
