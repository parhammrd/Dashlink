import * as React from 'react';
import Typography from '@mui/material/Typography';
import BasicChipList from '../components/TagChips';
import BasicTable from '../components/DataGrids';
import { fetchRecentUrls } from '../components/apiService';

import { auth } from '../../auth';

export default async function HomePage() {
  const session = await auth();

  let url_data: { url: string; scraped: boolean; }[] = [];
  let url_error = null;

  try {
    url_data = await fetchRecentUrls();
  } catch (err) {
    url_error = err instanceof Error ? err.message : 'Failed to load data';
  }

  return (    
    <div>
      <div>
      <Typography variant="h6">Your Tags</Typography>
      <BasicChipList />
      </div>
      <div>
      <Typography variant="h6">Recently Added</Typography>
      {url_error ? (
          <div>Error: {url_error}</div>
        ) : (
          <BasicTable data={url_data} />
        )}
      </div>
    </div>
  );
}
