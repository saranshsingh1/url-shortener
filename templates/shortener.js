let originalLinkContainer = document.getElementById("main-url"),
    originalButton = document.getElementById("original-link"),
    shortLinkContainer = document.getElementById("short-url"),
    shortenButton = document.getElementById("shorten-link");

// Add event listener to the Shorten URL button
shortenButton.addEventListener("click", async () => {
    let data = document.getElementById("original-url").value;

    shortLinkContainer.innerHTML = ``;
    originalLinkContainer.innerHTML = ``;

    try {
        let response = await fetch(`{{ shorten_url_post_link }}`, {
            method: "POST",
            cache: "no-cache",
            headers: {
                "Accept": "application/json",
                "Content-Type": "application/json",
            },
            body: JSON.stringify({"url": data})
        });

        // If the backend throws an exception
        // throw it again to be handled in the
        // catch block
        if (!response.ok) {
            throw await response.json();
        }

        let result = await response.json();

        originalLinkContainer.innerHTML = ``;
        shortLinkContainer.innerHTML = `Your shortened URL -
        <a href="${result['shortened_url']}" target="_blank" rel="noopener noreferrer nofollow">
            ${result['shortened_url']}
        </a>`;

    } catch (e) {
        console.warn(`Exception when fetching the shortened URL: ${e}`);
        // backend always throws the exception as a json object
        // with the information in the "detail" key.
        shortLinkContainer.innerText = e["detail"];
    }
});

// Add event listener to the Get original URL button
originalButton.addEventListener("click", async () => {
    let data = document.getElementById("original-url").value;

    shortLinkContainer.innerHTML = ``;
    originalLinkContainer.innerHTML = ``;

    try {
        let response = await fetch(`{{ original_url_post_link }}`, {
            method: "POST",
            cache: "no-cache",
            headers: {
                "Accept": "application/json",
                "Content-Type": "application/json",
            },
            body: JSON.stringify({"url": data})
        });

        // If the backend throws an exception
        // throw it again to be handled in the
        // catch block
        if (!response.ok) {
            throw await response.json();
        }

        let result = await response.json();

        shortLinkContainer.innerHTML = ``;
        originalLinkContainer.innerHTML = `Your original URL -
        <a href="${result['longer_url']}" target="_blank" rel="noopener noreferrer nofollow">
            ${result['longer_url']}
        </a>`;

    } catch (e) {
        console.warn(`Exception when fetching the shortened URL: ${e}`);
        // backend always throws the exception as a json object
        // with the information in the "detail" key.
        originalLinkContainer.innerText = e["detail"];
    }
});
