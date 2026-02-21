using System;
using System.Collections.Generic;
using UnityEngine;

namespace Universe.Codex
{
    [Serializable]
    public class CodexEvent
    {
        public string type;
        public string details;
        public string timestamp;
    }

    public class CodexEventLogger : MonoBehaviour
    {
        public List<CodexEvent> events = new List<CodexEvent>();

        public void Log(string type, string details)
        {
            events.Add(new CodexEvent
            {
                type = type,
                details = details,
                timestamp = DateTime.UtcNow.ToString("o")
            });
        }

        public string BuildAiPromptSeed() => $"Generate world events from {events.Count} logged events.";
    }
}
