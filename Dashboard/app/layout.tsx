import * as React from 'react';
import { AppProvider } from '@toolpad/core/nextjs';
import { AppRouterCacheProvider } from '@mui/material-nextjs/v14-appRouter';
import HomeIcon from '@mui/icons-material/Home';
import SourceIcon from '@mui/icons-material/Source';
import AccountBoxIcon from '@mui/icons-material/AccountBox';
import type { Navigation } from '@toolpad/core';
import { SessionProvider, signIn, signOut } from 'next-auth/react';
import { auth } from '../auth';
import theme from '../theme';

const NAVIGATION: Navigation = [
  {
    kind: 'header',
    title: 'Dashboard',
  },
  {
    segment: '',
    title: 'Home',
    icon: <HomeIcon />,
  },
  {
    segment: 'content',
    title: 'Content',
    icon: <SourceIcon />,
  },
  {
    segment: 'account',
    title: 'Account',
    icon: <AccountBoxIcon />,
  },
];

const BRANDING = {
  title: 'Dashlink App',
};


const AUTHENTICATION = {
  signIn,
  signOut,
};


export default async function RootLayout(props: { children: React.ReactNode }) {
  const session = await auth();

  return (
    <html lang="en" data-toolpad-color-scheme="light" suppressHydrationWarning>
      <body>
        <SessionProvider session={session}>
          <AppRouterCacheProvider options={{ enableCssLayer: true }}>
            <AppProvider
              navigation={NAVIGATION}
              branding={BRANDING}
              session={session}
              authentication={AUTHENTICATION}
              theme={theme}
            >
              {props.children}
            </AppProvider>
          </AppRouterCacheProvider>
        </SessionProvider>
      </body>
    </html>
  );
}
