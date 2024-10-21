import { useEffect, useState } from 'react';
import { fetchRecentUrls } from './apiService';

export const useRecentUrls = () => {
    const [data, setData] = useState<{ url: string; scraped: boolean }[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const loadData = async () => {
            try {
                const urls = await fetchRecentUrls();
                setData(urls);
            } catch (err) {
                setError(err instanceof Error ? err.message : 'An unknown error occurred');
            } finally {
                setLoading(false);
            }
        };

        loadData();
    }, []);

    return { data, loading, error };
};