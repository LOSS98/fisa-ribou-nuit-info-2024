import React, { useState, useEffect } from 'react';
import { Card } from "@/components/ui/card";
import { Trophy, Medal } from 'lucide-react';
import {
    Table,
    TableBody,
    TableCell,
    TableHead,
    TableHeader,
    TableRow,
} from "@/components/ui/table";

interface StreakEntry {
    id: number;
    pseudo: string;
    streak: number;
    date: string;
}

export const Leaderboard: React.FC = () => {
    const [streaks, setStreaks] = useState<StreakEntry[]>([]);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        fetchStreaks();
    }, []);

    const fetchStreaks = async () => {
        try {
            setIsLoading(true);
            const response = await fetch('https://fisa-ribou-nuit-info-2024.onrender.com/api/streaks');
            if (!response.ok) throw new Error('Failed to fetch streaks');
            const data = await response.json();

            // Sort streaks by highest to lowest
            const sortedStreaks = data.sort((a: StreakEntry, b: StreakEntry) => b.streak - a.streak);
            setStreaks(sortedStreaks);
        } catch (err) {
            setError('Failed to load leaderboard data');
            console.error(err);
        } finally {
            setIsLoading(false);
        }
    };

    const formatDate = (dateString: string) => {
        const date = new Date(dateString);
        return date.toLocaleDateString('fr-FR', {
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        });
    };

    const getMedalColor = (position: number) => {
        switch (position) {
            case 0: return 'text-yellow-400'; // Gold
            case 1: return 'text-gray-400';   // Silver
            case 2: return 'text-amber-600';  // Bronze
            default: return 'text-gray-400';
        }
    };

    if (isLoading) return (
        <div className="flex justify-center items-center min-h-[400px]">
            <div className="text-xl text-gray-500">Loading leaderboard...</div>
        </div>
    );

    if (error) return (
        <div className="flex justify-center items-center min-h-[400px]">
            <div className="text-xl text-red-500">{error}</div>
        </div>
    );

    return (
        <div className="container mx-auto py-8 px-4">
            <div className="flex items-center justify-between mb-6">
                <h1 className="text-3xl font-bold">Hall of Fame</h1>
                <Trophy className="h-8 w-8 text-yellow-400" />
            </div>

            <Card className="overflow-hidden">
                <Table>
                    <TableHeader>
                        <TableRow>
                            <TableHead className="w-16">Rank</TableHead>
                            <TableHead>Player</TableHead>
                            <TableHead className="text-right">Streak</TableHead>
                            <TableHead className="text-right">Date</TableHead>
                        </TableRow>
                    </TableHeader>
                    <TableBody>
                        {streaks.map((entry, index) => (
                            <TableRow
                                key={entry.id}
                                className={index < 3 ? 'font-medium' : ''}
                            >
                                <TableCell className="font-medium">
                                    <div className="flex items-center gap-2">
                                        {index < 3 ? (
                                            <Medal className={`h-5 w-5 ${getMedalColor(index)}`} />
                                        ) : (
                                            <span className="pl-7">{index + 1}</span>
                                        )}
                                    </div>
                                </TableCell>
                                <TableCell>{entry.pseudo}</TableCell>
                                <TableCell className="text-right">{entry.streak}</TableCell>
                                <TableCell className="text-right">{formatDate(entry.date)}</TableCell>
                            </TableRow>
                        ))}
                    </TableBody>
                </Table>
            </Card>
        </div>
    );
};