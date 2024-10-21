'use client';
import * as React from 'react';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';
import { Box } from '@mui/material';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import CancelIcon from '@mui/icons-material/Cancel';
import { green, red } from '@mui/material/colors';
import { useRecentUrls } from './useRecentUrls';

interface RowData {
    url: string;
    scraped: boolean;
}

interface BasicTableProps {
    data: RowData[];
}

export default function BasicTable({ data }: BasicTableProps) {
    return (
        <Box sx={{ margin: 1 }}>
            <TableContainer component={Paper}>
            <Table sx={{ minWidth: 650 }} aria-label="simple table">
            <TableHead>
                <TableRow>
                <TableCell>Url</TableCell>
                <TableCell align="right">Scraped</TableCell>
                </TableRow>
            </TableHead>
            <TableBody>
                {data.map((row) => (
                <TableRow
                    key={row.url}
                    sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
                >
                        <TableCell
                    component="th"
                    scope="row"
                    sx={{
                        maxWidth: 300,
                        overflow: 'hidden',
                        textOverflow: 'ellipsis',
                        whiteSpace: 'nowrap',
                    }}
                    >
                    {row.url}
                    </TableCell>
                    <TableCell align="right">
                    {row.scraped ? (
                        <CheckCircleIcon sx={{ color: green[500] }} />
                    ) : (
                        <CancelIcon sx={{ color: red[500] }} />
                    )}
                    </TableCell>
                </TableRow>
                ))}
            </TableBody>
            </Table>
        </TableContainer>
        </Box>
    );
}