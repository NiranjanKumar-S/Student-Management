/**
 * EduTrack - Dashboard Charts Visualization using Chart.js
 */

document.addEventListener('DOMContentLoaded', async () => {
    const deptCanvas = document.getElementById('deptChart');
    const yearCanvas = document.getElementById('yearChart');

    if (!deptCanvas || !yearCanvas) return;

    try {
        const response = await fetch('/api/stats');
        if (!response.ok) throw new Error('Failed to load chart data');
        const stats = await response.json();

        // 1. Department Distribution Chart (Doughnut)
        const deptCtx = deptCanvas.getContext('2d');
        const deptColors = [
            '#6366f1', // Indigo
            '#06b6d4', // Cyan
            '#3b82f6', // Blue
            '#10b981', // Emerald
            '#f59e0b', // Amber
            '#8b5cf6', // Violet
            '#ec4899', // Pink
            '#14b8a6'  // Teal
        ];

        new Chart(deptCtx, {
            type: 'doughnut',
            data: {
                labels: stats.departments.labels,
                datasets: [{
                    data: stats.departments.data,
                    backgroundColor: deptColors.slice(0, stats.departments.labels.length),
                    borderWidth: 2,
                    borderColor: '#ffffff',
                    hoverOffset: 6
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            boxWidth: 12,
                            padding: 14,
                            font: {
                                size: 11,
                                family: "'Plus Jakarta Sans', sans-serif"
                            },
                            color: '#475569'
                        }
                    },
                    tooltip: {
                        backgroundColor: '#1e293b',
                        titleFont: { size: 12, family: "'Plus Jakarta Sans', sans-serif" },
                        bodyFont: { size: 12, family: "'Plus Jakarta Sans', sans-serif" },
                        padding: 10,
                        cornerRadius: 8,
                        callbacks: {
                            label: function (context) {
                                const total = context.dataset.data.reduce((a, b) => a + b, 0);
                                const val = context.raw || 0;
                                const pct = total > 0 ? ((val / total) * 100).toFixed(1) : 0;
                                return ` ${val} Students (${pct}%)`;
                            }
                        }
                    }
                },
                cutout: '68%'
            }
        });

        // 2. Year & Semester Cohort Distribution (Bar Chart)
        const yearCtx = yearCanvas.getContext('2d');
        new Chart(yearCtx, {
            type: 'bar',
            data: {
                labels: stats.years.labels,
                datasets: [{
                    label: 'Enrolled Students',
                    data: stats.years.data,
                    backgroundColor: 'rgba(99, 102, 241, 0.85)',
                    hoverBackgroundColor: '#4f46e5',
                    borderRadius: 6,
                    borderSkipped: false
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    },
                    tooltip: {
                        backgroundColor: '#1e293b',
                        padding: 10,
                        cornerRadius: 8,
                        callbacks: {
                            label: (context) => ` ${context.raw} Students`
                        }
                    }
                },
                scales: {
                    x: {
                        grid: {
                            display: false
                        },
                        ticks: {
                            font: {
                                size: 11,
                                family: "'Plus Jakarta Sans', sans-serif"
                            },
                            color: '#64748b'
                        }
                    },
                    y: {
                        beginAtZero: true,
                        ticks: {
                            stepSize: 1,
                            precision: 0,
                            font: {
                                size: 11,
                                family: "'Plus Jakarta Sans', sans-serif"
                            },
                            color: '#64748b'
                        },
                        grid: {
                            color: '#f1f5f9'
                        }
                    }
                }
            }
        });

    } catch (err) {
        console.error('Error rendering dashboard analytics charts:', err);
    }
});
