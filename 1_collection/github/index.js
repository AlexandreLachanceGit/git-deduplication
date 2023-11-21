import { Octokit } from "octokit";

async function fetchGitHubRepositories() {
    const octokit = new Octokit({
        auth: process.env.TOKEN,
    });


    let allItems = [];
    let dates = ["<2020-01-01", "2020-01-01..2022-01-01", ">2022-01-01"]

    for (const d of dates) {
        console.error("Starting " + d)
        const perPage = 100; // Adjust the number of items per page as needed
        let page = 1;;
        while (true) {
            const queryString = 'q=' + encodeURIComponent('language:p4 fork:true created:' + d);
            // Add the page and per_page parameters to the query string
            const fullQueryString = `${queryString}&page=${page}&per_page=${perPage}`;

            try {
                const response = await octokit.request("GET /search/repositories?" + fullQueryString, {
                    headers: {
                        'X-GitHub-Api-Version': '2022-11-28'
                    }
                });

                if (response.data.items.length === 0) {
                    // No more results, break the loop
                    break;
                }

                // Append the items from the current page to the allItems array
                allItems = allItems.concat(response.data.items);

                // Increment the page number for the next request
                page++;
                console.error('Total repositories collected:', allItems.length);
            } catch (error) {
                console.error('Error fetching data:', error);
                break;
            }
        }
    }

    console.error(`Total items: ${allItems.length}`);
    console.log(JSON.stringify(allItems));
}

fetchGitHubRepositories();
