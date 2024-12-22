// NOTE: var anime must be defined in the html file in script tag

const build_graphql_query = (anime_name) => {
    return `
        query {
            Media (search: "${anime_name}", type: ANIME) {
                bannerImage
                coverImage{
                    extraLarge
                }
                status
                averageScore
            }
        }
    `;
};

const fetch_graphql_query = async (query) => {
    const url = "https://graphql.anilist.co";

    const options = {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            Accept: "application/json",
        },
        body: JSON.stringify({
            query: query,
        }),
    };

    const response = await fetch(url, options);
    const data = await response.json();
    return data;
};

const set_data = (anime_data) => {
    const anime_image = document.querySelector(".banner-container");
    const anime_status = document.querySelector(".anime-status");
    const anime_rating = document.querySelector(".anime-rating");

    try {
        if (window.innerWidth > 600) {
            anime_image.style.backgroundImage =
                "url(" + anime_data.bannerImage + ")";
        } else {
            anime_image.style.backgroundImage =
                "url(" + anime_data.coverImage.extraLarge + ")";
        }

        anime_status.innerText = `Status: ${anime_data.status}`;
        anime_rating.innerText = `Rating: ${anime_data.averageScore}%`;
    } catch (error) {
        // console.error(error);
    }
};

const main = async () => {
    const query = build_graphql_query(anime.title);
    const data = await fetch_graphql_query(query);

    if (data.errors === undefined) {
        set_data(data.data.Media);
    }
};

if (anime) {
    main();
}

// table sorter
function sortTableByColumn(table, column, asc = true) {
    const dirModifier = asc ? 1 : -1;
    const tBody = table.tBodies[0];
    const rows = Array.from(tBody.querySelectorAll("tr"));

    const sortedRows = rows.sort((a, b) => {
        const aColText = a
            .querySelector(`td:nth-child(${column + 1})`)
            .textContent.trim();
        const bColText = b
            .querySelector(`td:nth-child(${column + 1})`)
            .textContent.trim();
        if (isNaN(parseFloat(aColText)) && isNaN(parseFloat(bColText))) {
            return aColText > bColText ? 1 * dirModifier : -1 * dirModifier;
        }
        return +aColText > +bColText ? 1 * dirModifier : -1 * dirModifier;
    });

    while (tBody.firstChild) {
        tBody.removeChild(tBody.firstChild);
    }

    tBody.append(...sortedRows);

    table
        .querySelectorAll("th")
        .forEach((th) => th.classList.remove("th-sort-asc", "th-sort-desc"));
    table
        .querySelector(`th:nth-child(${column + 1})`)
        .classList.toggle("th-sort-asc", asc);
    table
        .querySelector(`th:nth-child(${column + 1})`)
        .classList.toggle("th-sort-desc", !asc);
}

document.querySelectorAll(".table-sortable th").forEach((headerCell) => {
    headerCell.addEventListener("click", () => {
        const tableElement =
            headerCell.parentElement.parentElement.parentElement;
        const headerIndex = Array.prototype.indexOf.call(
            headerCell.parentElement.children,
            headerCell
        );
        const currentIsAscending = headerCell.classList.contains("th-sort-asc");

        sortTableByColumn(tableElement, headerIndex, !currentIsAscending);
    });
});

// scroll detector
var lastScrollTop = 0;
var header = document.querySelector("header");
var scroll_button = document.querySelector(".scroll-button");

window.addEventListener(
    "scroll",
    function () {
        var st = window.scrollY || document.documentElement.scrollTop;
        if (st > lastScrollTop && st > 100) {
            // 100 is hardcoded based on navbar height
            header.style.transform = "translateY(-100%)";
            scroll_button.style.transform = "translateY(200%)";
        } else {
            header.style.transform = "translateY(0%)";
            header.style.opacity = 1;
            scroll_button.style.transform = "translateY(0%)";
        }
        if (st < 100) {
            header.style.opacity = 0.5;
            scroll_button.style.transform = "translateY(200%)"; // Cause user already on top
        }
        lastScrollTop = st <= 0 ? 0 : st; // For Mobile or negative scrolling
    },
    false
);

// scroll to top
// scroll_button already defined above
scroll_button.addEventListener("click", () => {
    window.scrollTo({ top: 0, behavior: "smooth" });
});
