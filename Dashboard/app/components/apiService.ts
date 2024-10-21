const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL;

export const fetchRecentUrls = async (): Promise<{ url: string; scraped: boolean }[]> => {
    const response = await fetch(`${API_BASE_URL}/recent-url/`);

    if (!response.ok) {
        throw new Error('Network response was not ok');
    }

    return response.json();
};