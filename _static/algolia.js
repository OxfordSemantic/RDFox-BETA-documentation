// Configuration
const applicationId = 'RKPMMD0DG4'
const apiSearchOnlyKey = '6123428be5e1aeb49d6f4b67bc58a509' // USE SEARCH ONLY KEY, NOT WRITE/ADMIN KEY
const indexName = 'prod_RDFox_docs'

const facetFilter = 'version:' + window.rdfoxDocsCurrentVersion

function rejectTerm(term) {
    return (
        term.toLowerCase().includes("nessus") ||
        term.toLowerCase().includes("wasscan")
    )
}

// Code
const searchClient = algoliasearch(applicationId, apiSearchOnlyKey);

const search = instantsearch({
    indexName,
    searchClient,
    searchFunction(helper) {
        if(helper.state.query) {
            helper.search();
        }
    },
});

const renderSearchBox = (renderOptions, isFirstRender) => {
    const { query, refine, clear, isSearchStalled, widgetParams } = renderOptions;

    if (isFirstRender) {
        const urlParams = new URLSearchParams(window.location.search);
        const input = document.querySelector('#rtd-search-form input[name=q]');
        const queryString = urlParams.get("q");
        if (!!queryString && !rejectTerm(queryString)) {
            refine(queryString);
        }
        input.value = queryString;
    }
}

const customSearchBox = instantsearch.connectors.connectSearchBox(renderSearchBox);

search.addWidgets([
    instantsearch.widgets.configure({
        facetFilters: [facetFilter],
        attributesToSnippet: ['content:30;']
    }),

    customSearchBox({
        container: '#rtd-search-form'
    }),

    ...((window.location.pathname.match(/^.*\/search(?:\.html)?$/g)) ? [instantsearch.widgets.hits({
        container: '#search-results',
        cssClasses: {
            list: "search"
        },
        templates: {
            item(hit, {html, components}) {
                splitHitUrl = hit.url.split("/")
                hitPage = splitHitUrl[splitHitUrl.length - 1]
                currentUrlCore = window.location.href.match(/.+\//)
                targetUrl = currentUrlCore + hitPage
                return html`
                    <a href="${targetUrl}">${hit.hierarchy.lvl3 || hit.hierarchy.lvl2 || hit.hierarchy.lvl1 || hit.hierarchy.lvl0}</a>
                    <div class="context">${components.Snippet({hit, attribute: 'content'})}</div>
                `
            },
            empty(results, { html }) {
                return html`No results for "${results.query}"`;
            }
        }
    })] : [])
]);

search.start();
