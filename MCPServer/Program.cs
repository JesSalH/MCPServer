using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;
using ModelContextProtocol;
using System.Net.Http.Headers;
using MCPServer.Tools;

var builder = Host.CreateEmptyApplicationBuilder(settings: null);

builder.Services.AddMcpServer()
    .WithStdioServerTransport()
    .WithToolsFromAssembly();

builder.Services.AddSingleton(_ =>
{
    var client = new HttpClient() { BaseAddress = new Uri("https://api.weather.gov") };
    client.DefaultRequestHeaders.UserAgent.Add(new ProductInfoHeaderValue("weather-tool", "1.0"));
    return client;
});

var app = builder.Build();

// Test WeatherTools methods
var httpClient = app.Services.GetRequiredService<HttpClient>();

// Test GetAlerts method
// try
// {
//     Console.WriteLine("Testing WeatherTools.GetAlerts() for California...");
//     var alertsResult = await WeatherTools.GetAlerts(httpClient, "CA");
//     Console.WriteLine("Alerts Result:");
//     Console.WriteLine(alertsResult);
//     Console.WriteLine("GetAlerts test completed successfully!");
// }
// catch (Exception ex)
// {
//     Console.WriteLine($"GetAlerts test failed with error: {ex.Message}");
//     Console.WriteLine($"Stack trace: {ex.StackTrace}");
// }
//
// Console.WriteLine("\n" + new string('-', 50) + "\n");
//
// // Test GetForecast method (using coordinates for San Francisco)
// try
// {
//     Console.WriteLine("Testing WeatherTools.GetForecast() for San Francisco (37.7749, -122.4194)...");
//     var forecastResult = await WeatherTools.GetForecast(httpClient, 37.7749, -122.4194);
//     Console.WriteLine("Forecast Result:");
//     Console.WriteLine(forecastResult);
//     Console.WriteLine("GetForecast test completed successfully!");
// }
// catch (Exception ex)
// {
//     Console.WriteLine($"GetForecast test failed with error: {ex.Message}");
//     Console.WriteLine($"Stack trace: {ex.StackTrace}");
// }

await app.RunAsync();