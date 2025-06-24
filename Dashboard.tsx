import React, { useEffect, useState } from 'react';
import {
  Grid,
  Paper,
  Typography,
  Box,
  Card,
  CardContent,
  Button,
  CircularProgress,
} from '@mui/material';
import {
  AccountBalance,
  TrendingUp,
  Payment,
  Assessment,
} from '@mui/icons-material';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  ArcElement,
} from 'chart.js';
import { Line, Doughnut } from 'react-chartjs-2';
import { useSelector } from 'react-redux';
import { RootState } from '../store';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  ArcElement
);

interface MetricData {
  title: string;
  value: string;
  icon: React.ReactNode;
  color: string;
}

interface ChartData {
  labels: string[];
  datasets: {
    label?: string;
    data: number[];
    borderColor?: string;
    backgroundColor?: string[];
    tension?: number;
  }[];
}

conost Dashboard: React.FC = () => {
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [balanceHistory, setBalanceHistory] = useState<ChartData>({
    labels: [],
    datasets: [],
  });
  const [spendingBreakdown, setSpendingBreakdown] = useState<ChartData>({
    labels: [],
    datasets: [],
  });

  const user = useSelector((state: RootState) => state.auth.user);

  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        // Simulate API call
        await new Promise((resolve) => setTimeout(resolve, 1000));

        setBalanceHistory({
          labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
          datasets: [
            {
              label: 'Account Balance',
              data: [1000, 1500, 1300, 1700, 2000, 2500],
              borderColor: 'rgb(75, 192, 192)',
              tension: 0.1,
            },
          ],
        });

        setSpendingBreakdown({
          labels: ['Savings', 'Bills', 'Shopping', 'Investment'],
          datasets: [
            {
              data: [30, 25, 20, 25],
              backgroundColor: [
                'rgb(54, 162, 235)',
                'rgb(255, 99, 132)',
                'rgb(255, 206, 86)',
                'rgb(75, 192, 192)',
              ],
            },
          ],
        });

        setIsLoading(false);
      } catch (error) {
        console.error('Error fetching dashboard data:', error);
        setIsLoading(false);
      }
    };

    fetchDashboardData();
  }, []);

  const metrics: MetricData[] = [
    {
      title: 'Current Balance',
      value: 'R 2,500.00',
      icon: <AccountBalance />,
      color: '#1976d2',
    },
    {
      title: 'Credit Score',
      value: '720',
      icon: <Assessment />,
      color: '#2e7d32',
    },
    {
      title: 'Monthly Savings',
      value: 'R 500.00',
      icon: <TrendingUp />,
      color: '#9c27b0',
    },
    {
      title: 'Next Payment Due',
      value: 'R 300.00',
      icon: <Payment />,
      color: '#ed6c02',
    },
  ];

  if (isLoading) {
    return (
      <Box
        sx={{
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'center',
          height: '100vh',
        }}
      >
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Welcome back, {user?.fullName || 'Guest'}
      </Typography>

      <Grid container spacing={3}>
        {metrics.map((metric) => (
          <Grid item xs={12} sm={6} md={3} key={metric.title}>
            <Card>
              <CardContent>
                <Box
                  sx={{
                    display: 'flex',
                    alignItems: 'center',
                    mb: 1,
                  }}
                >
                  <Box
                    sx={{
                      backgroundColor: `${metric.color}15`,
                      borderRadius: '50%',
                      p: 1,
                      mr: 2,
                    }}
                  >
                    {React.cloneElement(metric.icon as React.ReactElement, {
                      sx: { color: metric.color },
                    })}
                  </Box>
                  <Box>
                    <Typography color="textSecondary" variant="body2">
                      {metric.title}
                    </Typography>
                    <Typography variant="h6">{metric.value}</Typography>
                  </Box>
                </Box>
              </CardContent>
            </Card>
          </Grid>
        ))}

        <Grid item xs={12} md={8}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Balance History
            </Typography>
            <Line
              data={balanceHistory}
              options={{
                responsive: true,
                plugins: {
                  legend: {
                    position: 'top' as const,
                  },
                },
              }}
            />
          </Paper>
        </Grid>

        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Spending Breakdown
            </Typography>
            <Doughnut
              data={spendingBreakdown}
              options={{
                responsive: true,
                plugins: {
                  legend: {
                    position: 'bottom' as const,
                  },
                },
              }}
            />
          </Paper>
        </Grid>

        <Grid item xs={12}>
          <Paper sx={{ p: 3 }}>
            <Box
              sx={{
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center',
                mb: 2,
              }}
            >
              <Typography variant="h6">Quick Actions</Typography>
            </Box>
            <Grid container spacing={2}>
              <Grid item>
                <Button
                  variant="contained"
                  color="primary"
                  startIcon={<Payment />}
                >
                  New Payment
                </Button>
              </Grid>
              <Grid item>
                <Button
                  variant="contained"
                  color="secondary"
                  startIcon={<AccountBalance />}
                >
                  Apply for Loan
                </Button>
              </Grid>
              <Grid item>
                <Button
                  variant="contained"
                  color="success"
                  startIcon={<TrendingUp />}
                >
                  Start Saving
                </Button>
              </Grid>
            </Grid>
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
};

export default Dashboard; 
