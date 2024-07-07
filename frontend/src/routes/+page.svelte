<script>
    import { onMount } from "svelte";
    
    let data = "nothing";

    async function getVals() {
        const url = "https://sheets.googleapis.com/v4/spreadsheets/1drXUBYdQZDJldpvW0bRcx9EVS9THcYITYQK81pgXnX8"
        try {
            const res = await fetch(url);
            if (!res.ok) {
                throw new Error("Url fetching didn't work");
            }
            const resData = await res.json();
            data = resData;
        } catch (error) {
            console.log("Error: " + error);
        }
    }

    onMount(() => { getVals(); });

</script>

<h1>Welcome to SvelteKit</h1>
<p>Visit <a href="https://kit.svelte.dev">kit.svelte.dev</a> to read the documentation</p>
<p>
    {data}
</p>
