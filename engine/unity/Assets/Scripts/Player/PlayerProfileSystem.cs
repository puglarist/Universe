using System;
using System.IO;
using UnityEngine;

namespace Universe.Player
{
    [Serializable]
    public class PlayerProfile
    {
        public string username = "PlayerOne";
        public int level = 1;
        public int strength = 5;
        public int stamina = 5;
        public string avatarTexturePath;
    }

    public class PlayerProfileSystem : MonoBehaviour
    {
        public PlayerProfile profile = new PlayerProfile();
        private string SavePath => Path.Combine(Application.persistentDataPath, "player_profile.json");

        public void Save()
        {
            File.WriteAllText(SavePath, JsonUtility.ToJson(profile, true));
            Debug.Log($"Profile saved: {SavePath}");
        }

        public void Load()
        {
            if (!File.Exists(SavePath)) return;
            profile = JsonUtility.FromJson<PlayerProfile>(File.ReadAllText(SavePath));
            Debug.Log("Profile loaded.");
        }
    }
}
