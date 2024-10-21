'use client';
import * as React from 'react';
import Chip from '@mui/material/Chip';
import Stack from '@mui/material/Stack';
import Button from '@mui/material/Button';
import { Box } from '@mui/material';

export default function BasicChipList() {
    return (
    <Box sx={{ margin: 1 }}>
        <Stack direction="row" sx={{ flexWrap: 'wrap', gap: 1 }}>
          <Chip label="Chip" variant="outlined" />
          <Chip label="Chip" variant="outlined" />
          <Chip label="Chip" variant="outlined" />
          <Button variant="outlined" sx={{ height: '32px', marginBottom: 1 }}>
            + Add Tag
          </Button>
        </Stack>
      </Box>
    );
}