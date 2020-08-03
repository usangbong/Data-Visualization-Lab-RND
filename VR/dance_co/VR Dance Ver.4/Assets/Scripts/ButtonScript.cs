using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class ButtonScript : MonoBehaviour
{
    public GameObject obj;
    SavePosTest spt;

    void Start()
    {
        spt = obj.GetComponent<SavePosTest>();
    }

    public void OnClick()
    {
        spt.setButton(true);
    }

    public void Quit()
    {
        UnityEditor.EditorApplication.isPlaying = false;
    }
}
