using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;
using Valve.VR;

public class ChangLine : MonoBehaviour
{
    public SteamVR_Input_Sources handType;
    public SteamVR_Action_Boolean grabgripAction;

    void Update()
    {
        if (grabgripAction.GetStateDown(handType))
        {
            SceneManager.LoadScene("Director Line Scene");
        }
    }
}
