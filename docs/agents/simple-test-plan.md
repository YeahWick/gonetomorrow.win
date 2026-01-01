# Simple Testing Plan for Updates

## Objective
Create a straightforward testing process for site updates that is easy to understand and execute.

## Approach

### 1. Branch Strategy
- Use `main` branch for production
- Create a `testing` branch for testing updates
- Use pull requests to merge changes into `testing` branch

### 2. Testing Process
1. Make changes in a feature branch
2. Create a PR to merge into `testing` branch
3. Once approved, merge to `testing` branch
4. Temporarily configure GitHub Pages to deploy from `testing` branch
5. Verify the site works correctly at the test URL
6. Change GitHub Pages back to deploy from `main` branch
7. Create a PR to merge the feature branch into `main`
8. Deploy the changes by merging to `main`

### 3. Alternative: Testing as Default
Alternatively, configure GitHub Pages to deploy from the `testing` branch by default:
- All changes are visible immediately on the live site when merged to `testing`
- For production releases, temporarily change deployment to `main` branch
- This approach is simpler but means the live site shows testing content

## Benefits
- Extremely simple to understand and execute
- No need for complex GitHub Actions workflows
- Minimal configuration required
- Works with GitHub Pages limitations

## Considerations
- Only one version can be published at a time
- Requires manual switching of the publishing source
- Testing period is limited to when the publishing source is set to `testing`

## Implementation
1. Create the `testing` branch from `main`
2. Configure GitHub Pages to deploy from the chosen branch (either `main` or `testing`)
3. Update contributor documentation to explain the testing process
4. Begin using pull requests for all changes