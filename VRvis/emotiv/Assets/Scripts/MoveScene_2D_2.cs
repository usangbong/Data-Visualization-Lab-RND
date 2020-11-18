using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;
using Valve.VR.InteractionSystem;

public class MoveScene_2D_2 : MonoBehaviour
{
    // Start is called before the first frame update

    private void Awake()
    {
        DontDestroyOnLoad(this.gameObject);
    }
    // Update is called once per frame
    void Update()
    {

        int idx = SceneManager.GetActiveScene().buildIndex;

        if(Input.GetKeyDown(KeyCode.RightArrow))
        {
            if(idx + 1 <= 28)
                SceneManager.LoadScene(idx + 1);
        }

        else if(Input.GetKeyDown(KeyCode.LeftArrow))
        {
            if(idx-1 >= 22)
                SceneManager.LoadScene(idx - 1);
        }

    }
}
