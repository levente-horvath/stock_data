<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use GuzzleHttp\Client;
use GuzzleHttp\Exception\RequestException;
use Illuminate\Support\Facades\Log;

class StockDataController extends Controller
{
    public function index(Request $request)
    {
        try {
            $client = new Client();
            // Ensure query parameters are properly retrieved
            $stockSymbol = $request->query('symbol', 'ANET');
            $days = $request->query('days', 100);
            $window = $request->query('window', 3);

            // Validate input parameters
            if (!is_string($stockSymbol) || !is_numeric($days) || !is_numeric($window)) {
                throw new \InvalidArgumentException('Invalid input parameters');
            }
        
            $stockSymbol = $request->input('symbol', 'ANET');
            $days = $request->input('days', 100);
            $window = $request->input('window', 3);
            
            // Construct API URL (base URL should be in config or .env)
            $apiUrl = "http://38.242.157.16:8000/plot_moving_average_plotly/{$stockSymbol}/{$days}/{$window}";
            $response = $client->get($apiUrl)->getBody()->getContents();
            
            // Decode the JSON response into an array for Plotly
        
            function isJson($string) {
                json_decode($string);
                return json_last_error() === JSON_ERROR_NONE;
             }
        
             

            $response = json_decode($response, true);
            
            $plotData = json_decode($response, true);
            // Check if decoding failed
            if (json_last_error() !== JSON_ERROR_NONE) {
                throw new \Exception('Invalid JSON response from API');
            }
        } catch (RequestException $e) {
            // Log network-related errors
            Log::error('API request failed: ' . $e->getMessage());
            $plotData = [
                'data' => [],
                'layout' => ['title' => 'Error fetching data']
            ];
        } catch (\Exception $e) {
            // Log other errors (e.g., JSON decoding issues)
            Log::error('Error processing API response: ' . $e->getMessage());
            $plotData = [
                'data' => [],
                'layout' => ['title' => 'Error processing data']
            ];
        }

        // Pass data to Inertia React component or return JSON if requested
        if ($request->wantsJson()) {
            return response()->json(['plotData' => $plotData]);
        }
        return inertia('stock', [
            'plotData' => $plotData
        ]);
    }
}