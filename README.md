# String Sorting Visualizer

An educational Streamlit app for exploring how different sorting algorithms order strings. It compares bubble sort, selection sort, and quick sort on the same input so learners can inspect each result and compare element comparisons, swaps, and sorting accuracy against Python's built-in `sorted()` function.

## Features

- Enter strings manually or choose from a bundled word list.
- Sort the same input with bubble sort, selection sort, and quick sort.
- View the sorted output, comparison count, swap count, and accuracy for each algorithm.
- See the input used for each comparison.

## Docker Hub credentials

GitHub Actions expects the Docker Hub credentials to be configured as GitHub repository secrets:

- `DOCKERHUB_USERNAME`
- `DOCKERHUB_TOKEN`

Add them in the repository's **Settings → Secrets and variables → Actions**. Store the Docker Hub access token as a secret; do not put credential values in this README or commit them to the repository.
