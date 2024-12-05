export interface Question {
    id: number;
    question: string;
    answer: "humain" | "océan" | "les deux";  // Only these three possible answers
}

export interface GameState {
    currentQuestion: number;
    streak: number;
    gameOver: boolean;
}