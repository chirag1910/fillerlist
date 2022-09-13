// image loader
let anime_name = document.querySelector(
    ".info-container .blur .anime-name"
).innerText;
let anime_image = document.querySelector(".banner-container");
let anime_status = document.querySelector(".anime-status");
let anime_rating = document.querySelector(".anime-rating");
get_image_src(anime_name, anime_image, anime_status, anime_rating);

function get_image_src(anime_name, anime_image, anime_status, anime_rating) {
    if (anime_name.includes("(")) {
        anime_name = anime_name.split("(")[0];
    }

    var query = `
        query ($search: String) {
            Media (search: $search, type: ANIME) {
                bannerImage
                coverImage{
                    extraLarge
                }
                status
                averageScore
            }
        }
    `;

    var variables = {
        search: anime_name,
    };

    var url = "https://graphql.anilist.co",
        options = {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                Accept: "application/json",
            },
            body: JSON.stringify({
                query: query,
                variables: variables,
            }),
        };

    fetch(url, options)
        .then(handleResponse)
        .then(handleData)
        .catch(handleError);

    function handleResponse(response) {
        return response.json().then(function (json) {
            return response.ok ? json : Promise.reject(json);
        });
    }

    function handleData(data) {
        if (window.innerWidth > 600) {
            anime_image.style.backgroundImage =
                "url(" + data["data"]["Media"]["bannerImage"] + ")";
        } else {
            anime_image.style.backgroundImage =
                "url(" +
                data["data"]["Media"]["coverImage"]["extraLarge"] +
                ")";
        }
        anime_status.innerText = `Status: ${
            data["data"]["Media"]["status"] || "N/A"
        }`;
        anime_rating.innerText = `Rating: ${
            data["data"]["Media"]["averageScore"] || "--"
        }%`;
    }

    function handleError(error) {
        anime_image.style.backgroundImage =
            "linear-gradient(to top, rgb(0,0,0,0.8), transparent), url('https://s4.anilist.co/file/anilistcdn/character/large/default.jpg')";
        anime_image.style.backgroundRepeat = "repeat";
        anime_image.style.backgroundSize = "auto";
    }
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
var header = document.querySelector(".header-wrapper");
var scroll_button = document.querySelector(".scroll-button");

window.addEventListener(
    "scroll",
    function () {
        var st = window.pageYOffset || document.documentElement.scrollTop;
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
