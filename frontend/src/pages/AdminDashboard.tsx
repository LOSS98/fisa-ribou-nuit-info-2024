import React, { useState, useEffect } from 'react';
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import {
    Table,
    TableBody,
    TableCell,
    TableHead,
    TableHeader,
    TableRow,
} from "@/components/ui/table";
import {
    Dialog,
    DialogContent,
    DialogHeader,
    DialogTitle,
    DialogFooter,
} from "@/components/ui/dialog";
import { Label } from "@/components/ui/label";
import { Pencil, Trash2, Plus } from 'lucide-react';
import {Question} from "@/lib/interfaces.ts";

const AdminDashboard: React.FC = () => {
    const [questions, setQuestions] = useState<Question[]>([]);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const [showEditDialog, setShowEditDialog] = useState(false);
    const [showAddDialog, setShowAddDialog] = useState(false);
    const [currentQuestion, setCurrentQuestion] = useState<Question | null>(null);
    const [newQuestion, setNewQuestion] = useState<Partial<Question>>({
        question: '',
        answer: "L'Humain"
    });

    useEffect(() => {
        fetchQuestions();
    }, []);

    const fetchQuestions = async () => {
        try {
            const response = await fetch('/api/admin/questions');
            if (!response.ok) throw new Error('Failed to fetch questions');
            const data = await response.json();
            setQuestions(data);
        } catch (err) {
            setError('Failed to load questions');
            console.error(err);
        } finally {
            setIsLoading(false);
        }
    };

    const handleEdit = (question: Question) => {
        setCurrentQuestion(question);
        setShowEditDialog(true);
    };

    const handleDelete = async (id: number) => {
        if (window.confirm('Are you sure you want to delete this question?')) {
            try {
                const response = await fetch(`/api/admin/questions/${id}`, {
                    method: 'DELETE',
                });
                if (!response.ok) throw new Error('Failed to delete question');
                setQuestions(questions.filter(q => q.id !== id));
            } catch (err) {
                setError('Failed to delete question');
                console.error(err);
            }
        }
    };

    const handleSave = async () => {
        if (!currentQuestion) return;

        try {
            const response = await fetch(`/api/admin/questions/${currentQuestion.id}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(currentQuestion),
            });
            if (!response.ok) throw new Error('Failed to update question');

            setQuestions(questions.map(q =>
                q.id === currentQuestion.id ? currentQuestion : q
            ));
            setShowEditDialog(false);
        } catch (err) {
            setError('Failed to update question');
            console.error(err);
        }
    };

    const handleAdd = async () => {
        try {
            const response = await fetch('/api/admin/questions', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(newQuestion),
            });
            if (!response.ok) throw new Error('Failed to add question');

            const addedQuestion = await response.json();
            setQuestions([...questions, addedQuestion]);
            setShowAddDialog(false);
            setNewQuestion({ question: '', answer: "L'Humain" });
        } catch (err) {
            setError('Failed to add question');
            console.error(err);
        }
    };

    if (isLoading) return <div className="p-8">Loading...</div>;
    if (error) return <div className="p-8 text-red-500">{error}</div>;

    return (
        <div className="p-8">
            <div className="flex justify-between items-center mb-6">
                <h1 className="text-3xl font-bold">Questions Management</h1>
                <Button onClick={() => setShowAddDialog(true)}>
                    <Plus className="mr-2 h-4 w-4" />
                    Add Question
                </Button>
            </div>

            <Card>
                <Table>
                    <TableHeader>
                        <TableRow>
                            <TableHead>ID</TableHead>
                            <TableHead>Question</TableHead>
                            <TableHead>Answer</TableHead>
                            <TableHead className="text-right">Actions</TableHead>
                        </TableRow>
                    </TableHeader>
                    <TableBody>
                        {questions.map((question) => (
                            <TableRow key={question.id}>
                                <TableCell>{question.id}</TableCell>
                                <TableCell>{question.question}</TableCell>
                                <TableCell>{question.answer}</TableCell>
                                <TableCell className="text-right">
                                    <Button
                                        variant="ghost"
                                        size="sm"
                                        onClick={() => handleEdit(question)}
                                        className="mr-2"
                                    >
                                        <Pencil className="h-4 w-4" />
                                    </Button>
                                    <Button
                                        variant="ghost"
                                        size="sm"
                                        onClick={() => handleDelete(question.id)}
                                    >
                                        <Trash2 className="h-4 w-4" />
                                    </Button>
                                </TableCell>
                            </TableRow>
                        ))}
                    </TableBody>
                </Table>
            </Card>

            {/* Edit Dialog */}
            <Dialog open={showEditDialog} onOpenChange={setShowEditDialog}>
                <DialogContent>
                    <DialogHeader>
                        <DialogTitle>Edit Question</DialogTitle>
                    </DialogHeader>
                    <div className="space-y-4">
                        <div>
                            <Label htmlFor="edit-question">Question</Label>
                            <Input
                                id="edit-question"
                                value={currentQuestion?.question || ''}
                                onChange={(e) => setCurrentQuestion(prev =>
                                    prev ? { ...prev, question: e.target.value } : null
                                )}
                            />
                        </div>
                        <div>
                            <Label htmlFor="edit-answer">Answer</Label>
                            <select
                                id="edit-answer"
                                className="w-full border rounded-md p-2"
                                value={currentQuestion?.answer || 'humain'}
                                onChange={(e) => setCurrentQuestion(prev =>
                                    prev ? { ...prev, answer: e.target.value as Question['answer'] } : null
                                )}
                            >
                                <option value="humain">L'Humain</option>
                                <option value="océan">L'Océan</option>
                                <option value="les deux">Les deux</option>
                            </select>
                        </div>
                    </div>
                    <DialogFooter>
                        <Button onClick={handleSave}>Save Changes</Button>
                    </DialogFooter>
                </DialogContent>
            </Dialog>

            {/* Add Dialog */}
            <Dialog open={showAddDialog} onOpenChange={setShowAddDialog}>
                <DialogContent>
                    <DialogHeader>
                        <DialogTitle>Add New Question</DialogTitle>
                    </DialogHeader>
                    <div className="space-y-4">
                        <div>
                            <Label htmlFor="new-question">Question</Label>
                            <Input
                                id="new-question"
                                value={newQuestion.question}
                                onChange={(e) => setNewQuestion(prev => ({ ...prev, question: e.target.value }))}
                            />
                        </div>
                        <div>
                            <Label htmlFor="new-answer">Answer</Label>
                            <select
                                id="new-answer"
                                className="w-full border rounded-md p-2"
                                value={newQuestion.answer}
                                onChange={(e) => setNewQuestion(prev => ({
                                    ...prev,
                                    answer: e.target.value as Question['answer']
                                }))}
                            >
                                <option value="humain">L'Humain</option>
                                <option value="océan">L'Océan</option>
                                <option value="les deux">Les deux</option>
                            </select>
                        </div>
                    </div>
                    <DialogFooter>
                        <Button onClick={handleAdd}>Add Question</Button>
                    </DialogFooter>
                </DialogContent>
            </Dialog>
        </div>
    );
};

export default AdminDashboard;