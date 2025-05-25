import React, { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert';
import { AlertCircle } from 'lucide-react';
import { cn } from '@/lib/utils';

interface AnalysisResult {
    result: string;
    explanation: string;
    confidence?: number;
}

const FakeNewsDetector: React.FC = () => {
    const [inputType, setInputType] = useState<'Text' | 'URL'>('Text');
    const [newsText, setNewsText] = useState('');
    const [newsUrl, setNewsUrl] = useState('');
    const [analysisResult, setAnalysisResult] = useState<AnalysisResult | null>(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const handleAnalyze = async () => {
        if (inputType === 'Text' && !newsText.trim()) {
            setError('Please enter the news text to analyze.');
            return;
        }
        if (inputType === 'URL' && !newsUrl.trim()) {
            setError('Please enter the URL of the news article.');
            return;
        }

        setError(null);
        setLoading(true);
        setAnalysisResult(null); // Clear previous results

        // Simulate analysis (replace with actual API call)
        try {
            // Simulate an API call with a delay
            await new Promise(resolve => setTimeout(resolve, 2000));

            // Simulate different results based on input
            let simulatedResult: AnalysisResult;
            if (inputType === 'Text') {
                if (newsText.toLowerCase().includes('fake') || newsText.toLowerCase().includes('unreliable')) {
                    simulatedResult = {
                        result: 'Likely Fake',
                        explanation: 'The text contains keywords often associated with unreliable information.',
                        confidence: 0.85,
                    };
                } else if (newsText.toLowerCase().includes('true') || newsText.toLowerCase().includes('credible')) {
                    simulatedResult = {
                        result: 'Likely Real',
                        explanation: 'The text contains keywords suggesting credible information.',
                        confidence: 0.92,
                    };
                } else {
                    simulatedResult = {
                        result: 'Uncertain',
                        explanation: 'Unable to determine with high confidence based on the input.',
                        confidence: 0.55,
                    };
                }
            } else { // URL
                 if (newsUrl.toLowerCase().includes('fake') || newsUrl.toLowerCase().includes('unreliable')) {
                    simulatedResult = {
                        result: 'Likely Fake',
                        explanation: 'The URL is associated with a source that has been known to spread misinformation.',
                        confidence: 0.78,
                    };
                } else if (newsUrl.toLowerCase().includes('true') || newsUrl.toLowerCase().includes('credible')) {
                    simulatedResult = {
                        result: 'Likely Real',
                        explanation: 'The URL is from a reputable news source.',
                        confidence: 0.95,
                    };
                }
                else {
                    simulatedResult = {
                        result: 'Uncertain',
                        explanation: 'The credibility of the URL could not be reliably determined.',
                        confidence: 0.62
                    }
                }
            }


            setAnalysisResult(simulatedResult);
        } catch (err: any) {
            setError(`An error occurred: ${err.message || 'Failed to analyze news.'}`);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="min-h-screen bg-gradient-to-br from-gray-900 to-gray-800 p-4 sm:p-8">
            <div className="max-w-3xl mx-auto space-y-6">
                <h1 className="text-3xl sm:text-4xl font-bold text-white text-center">
                    Fake News Detector
                </h1>

                <div className="bg-white/5 backdrop-blur-md rounded-xl shadow-lg p-4 sm:p-6 border border-white/10">
                    <div className="space-y-4">
                        <div className="flex flex-col sm:flex-row gap-4">
                            <Button
                                variant={inputType === 'Text' ? 'default' : 'outline'}
                                onClick={() => setInputType('Text')}
                                className={cn(
                                    "flex-1",
                                    "bg-white/10 text-white hover:bg-white/20",
                                    "border-white/20",
                                    "transition-colors duration-200"
                                )}
                                disabled={loading}
                            >
                                Text
                            </Button>
                            <Button
                                variant={inputType === 'URL' ? 'default' : 'outline'}
                                onClick={() => setInputType('URL')}
                                className={cn(
                                   "flex-1",
                                    "bg-white/10 text-white hover:bg-white/20",
                                    "border-white/20",
                                    "transition-colors duration-200"
                                )}
                                disabled={loading}
                            >
                                URL
                            </Button>
                        </div>

                        {inputType === 'Text' ? (
                            <Textarea
                                placeholder="Paste the news content here..."
                                value={newsText}
                                onChange={(e) => setNewsText(e.target.value)}
                                className="bg-black/20 text-white border-gray-700 placeholder:text-gray-400"
                                disabled={loading}
                                rows={6}
                            />
                        ) : (
                            <Input
                                type="url"
                                placeholder="Enter the URL of the news article..."
                                value={newsUrl}
                                onChange={(e) => setNewsUrl(e.target.value)}
                                className="bg-black/20 text-white border-gray-700 placeholder:text-gray-400"
                                disabled={loading}
                            />
                        )}

                        <Button
                            onClick={handleAnalyze}
                            disabled={loading}
                            className={cn(
                                "w-full bg-blue-500 text-white hover:bg-blue-600",
                                "transition-colors duration-200",
                                "py-3 sm:py-4 text-lg"
                            )}
                        >
                            {loading ? 'Analyzing...' : 'Analyze'}
                        </Button>

                        {error && (
                            <Alert variant="destructive" className="bg-red-500/10 text-red-400 border-red-500/20">
                                <AlertCircle className="h-4 w-4" />
                                <AlertTitle>Error</AlertTitle>
                                <AlertDescription>{error}</AlertDescription>
                            </Alert>
                        )}

                        {analysisResult && (
                            <div className="bg-white/5 backdrop-blur-md rounded-xl p-4 sm:p-6 border border-white/10">
                                <h2 className="text-xl font-semibold text-white mb-2">Analysis Result:</h2>
                                <div
                                    className={cn(
                                        "text-lg font-bold mb-2",
                                        analysisResult.result.includes('Fake') ? "text-red-400" :
                                            analysisResult.result.includes('Real') ? "text-green-400" :
                                                "text-yellow-400"
                                    )}
                                >
                                    {analysisResult.result}
                                </div>
                                 {analysisResult.confidence && (
                                    <p className="text-gray-300 mb-2">
                                        Confidence: {(analysisResult.confidence * 100).toFixed(2)}%
                                    </p>
                                )}
                                <p className="text-gray-300">
                                    {analysisResult.explanation}
                                </p>
                            </div>
                        )}
                    </div>
                </div>
            </div>
        </div>
    );
};

export default FakeNewsDetector;
