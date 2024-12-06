import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
    Dialog,
    DialogContent,
    DialogHeader,
    DialogTitle,
    DialogDescription,
    DialogFooter,
    DialogClose,
} from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card } from "@/components/ui/card";
import { Trophy, X } from 'lucide-react';
import {GameState, Question} from "@/lib/interfaces.ts";


const POSSIBLE_ANSWERS = ["L'Humain", "L'Océan", "Les deux"] as const;

const Quiz: React.FC = () => {
    const [questions, setQuestions] = useState<Question[]>([]);
    const [gameState, setGameState] = useState<GameState>({
        currentQuestion: 0,
        streak: 0,
        gameOver: false
    });
    const [playerName, setPlayerName] = useState<string>('');
    const [showNameDialog, setShowNameDialog] = useState<boolean>(true);
    const [isLoading, setIsLoading] = useState<boolean>(true);
    const [error, setError] = useState<string | null>(null);

    const navigate = useNavigate();

    useEffect(() => {
        const fetchQuestions = async (): Promise<void> => {
            try {
                setIsLoading(true);
                const response = await fetch('http://localhost:5000/api/quiz');
                if (!response.ok) {
                    console.error("HTTP error! status: " + response.statusText);
                    setError(`HTTP error! status: ${response.status}`);
                }
                const data = await response.json() as Question[];
                console.log("data:" + data);
                setQuestions(data);
            } catch (error) {
                setError(error instanceof Error ? error.message : 'An error occurred');
            } finally {
                setIsLoading(false);
            }
        };

        fetchQuestions();
    }, []);

    const handleNameSubmit = (e: React.FormEvent<HTMLFormElement>): void => {
        e.preventDefault();
        if (playerName.trim()) {
            setShowNameDialog(false);
        }
    };

    const handleAnswerSelect = (selectedAnswer: string): void => {
        const isCorrect = selectedAnswer === questions[gameState.currentQuestion].answer;

        if (isCorrect) {
            if (gameState.currentQuestion + 1 < questions.length) {
                setGameState(prev => ({
                    ...prev,
                    currentQuestion: prev.currentQuestion + 1,
                    streak: prev.streak + 1
                }));
            } else {
                setGameState(prev => ({
                    ...prev,
                    gameOver: true,
                    streak: prev.streak + 1
                }));
            }
        } else {
            setGameState(prev => ({
                ...prev,
                gameOver: true
            }));
        }
    };

    const handlePlayAgain = (): void => {
        setGameState({
            currentQuestion: 0,
            streak: 0,
            gameOver: false
        });
    };

    const handleDialogClose = () => {
        navigate('/');
    }

    if (isLoading) {
        return (
            <div className="flex items-center justify-center min-h-screen">
                <p className="text-xl">Loading questions...</p>
            </div>
        );
    }

    if (error) {
        return (
            <div className="flex items-center justify-center min-h-screen">
                <p className="text-xl text-red-600">Error: {error}</p>
            </div>
        );
    }

    return (
        <div className="flex-grow bg-gray-100 p-8">
            <Dialog open={showNameDialog} onOpenChange={(open) => {
                if (!open) handleDialogClose();
            }}>
                <DialogContent className="sm:max-w-[425px] [&>button]:hidden">
                    <DialogHeader>
                        <div className="flex justify-between items-center">
                            <DialogTitle>Welcome to Burger Quiz!</DialogTitle>
                            <DialogClose onClick={handleDialogClose} className="bg-white">
                                <X className="h-4 w-4"/>
                            </DialogClose>
                        </div>
                        <DialogDescription>
                            Please enter your name to start the game.
                        </DialogDescription>
                    </DialogHeader>
                    <form onSubmit={handleNameSubmit} className="space-y-4">
                        <Input
                            placeholder="Enter your name"
                            value={playerName}
                            onChange={(e: React.ChangeEvent<HTMLInputElement>) => setPlayerName(e.target.value)}
                            required
                        />
                        <DialogFooter>
                            <Button type="submit">Start Game</Button>
                        </DialogFooter>
                    </form>
                </DialogContent>
            </Dialog>

            {!showNameDialog && questions.length > 0 && (
                <div className="max-w-2xl mx-auto">
                    <div className="flex justify-between items-center mb-8">
                        <h1 className="text-3xl font-bold">Burger Quiz</h1>
                        <div className="flex items-center gap-2">
                            <Trophy className="text-yellow-500" />
                            <span className="text-xl font-bold">Streak: {gameState.streak}</span>
                        </div>
                    </div>

                    {gameState.gameOver ? (
                        <Card className="p-8 text-center">
                            <h2 className="text-2xl font-bold mb-4">Game Over, {playerName}!</h2>
                            <p className="text-xl mb-4">Final Streak: {gameState.streak}</p>
                            <div className="space-x-4">
                                <Button onClick={handlePlayAgain}>Play Again</Button>
                                <Button variant="outline" onClick={() => navigate('/')}>
                                    Exit to Menu
                                </Button>
                            </div>
                        </Card>
                    ) : (
                        <Card className="p-8">
                            <div className="mb-6">
                                <h3 className="text-lg font-medium mb-2">
                                    Question {gameState.currentQuestion + 1} of {questions.length}
                                </h3>
                                <p className="text-xl mb-6">{questions[gameState.currentQuestion].question}</p>
                                <div className="grid grid-cols-1 gap-4">
                                    {POSSIBLE_ANSWERS.map((answer) => (
                                        <Button
                                            key={answer}
                                            onClick={() => handleAnswerSelect(answer)}
                                            className="h-16 text-lg"
                                            variant="secondary"
                                        >
                                            {answer}
                                        </Button>
                                    ))}
                                </div>
                            </div>
                        </Card>
                    )}
                </div>
            )}
        </div>
    );
};

export default Quiz;