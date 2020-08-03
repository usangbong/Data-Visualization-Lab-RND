using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;

public class Final : MonoBehaviour
{
    public GameObject Character, puzzlewhite2_1;
    public GameObject _90, blue_triangle, _4cube;
    public GameObject spring_with_stick, flat_circle5;
    public GameObject flat_circle5_in_background, puzzle_blue;
    public GameObject half, eye, stick1_L, stick2_L, stick5_L, stick6_L, top_triangle;
    public GameObject green_and_orange, left_blackmodel;
    public GameObject blue, yellow, red_sphere, under_wave;
    public GameObject right_bottom_triangle, smile, puzzle_white1;
    public GameObject puzzle_white2, puzzle_white2_2, puzzle_whilte2_3, puzzlewhilte2_4;
    public GameObject red_wave, color_wave, Heeart, arrow, red_Cube;
    public GameObject blackStick_bottom, longStick, blackStick_bottom_1;
    public GameObject sitck1_M_14, puzzleSphere_blue1, puzzleSphere_blue2;
    public GameObject puzzleSphere_orange, puzzle_torus, puzzle_grayCube;
    public GameObject sphere_beige, sphere_pupple, cube_3, stick_M;
    public GameObject stick1_yellow_M, stick_bottom, stick_bottom2, stick_bottom3;
    public GameObject brownStick_bottom, brownStick_bottom2;
    public GameObject redCube2, front_stick1, front_stick2;
    public GameObject black_cube, blackCube2, blackCube3, blackCube4;
    public GameObject stick_M1, stick_M2, stick_M3, stick_M4, stick_M5;
    public GameObject stick_M6, stick_M7, stick_M8, top_blueSphere;
    public GameObject top_redSphere, stick_M9, stick_M10, stick_M11;
    public GameObject stick_M12, stick_M13, yellowCube, ring;
    public GameObject puzzle1, puzzle2, brownWave, arrowBackground;
    public GameObject stick3_L, stick4_L, colorRing1, colorRing2, colorRing3;
    public GameObject sp1, sp2, sp3, sp4, sp5, nullParent;

    public Material black, bluee, red, deepOrange, orange, green, beige, sphereRed, stringBrown;
    public Material yelloww, brown, gray, yellowStick, _90out, stickMat, white, redHeart, spherePupple;
    public Material blue_sphere, triangleOrange, redSpYellow;

    List<GameObject> arrowList = new List<GameObject>();

    public bool timeFin, arrowParentNull;
    public float time;
    public float sp;
    float speed;
    bool colorBool;

    private void Start()
    {
        time = 0;
        speed = sp * Time.deltaTime;
        colorBool = false;
        timeFin = arrowParentNull = false;
        StartCoroutine(timeChecker());
    }

    private void Update()
    {
        if (timeFin)
        {
            sp1.transform.DetachChildren();
            sp2.transform.DetachChildren();
            sp3.transform.DetachChildren();
            sp4.transform.DetachChildren();
            sp5.transform.DetachChildren();
            nullParent.transform.DetachChildren();
            if (!arrowParentNull || colorBool)
            {
                arrowList.Add(arrow.transform.GetChild(0).gameObject);
                arrowList.Add(arrow.transform.GetChild(1).gameObject);
                arrowList.Add(arrow.transform.GetChild(2).gameObject);

                arrow.transform.DetachChildren();
                for (int i=0;i<3;i++)
                {
                    arrowList[i].transform.SetParent(arrow.transform);
                }

                arrowParentNull = true;

                Character.transform.GetChild(2).gameObject.SetActive(false);
                Character.transform.GetChild(1).GetChild(8).GetComponent<Colliders>().enabled = false;

                for(int i=0;i<8;i++)
                {
                    Character.transform.GetChild(1).GetChild(i).gameObject.SetActive(false);
                }

                puzzle1.transform.GetChild(1).GetComponent<MeshRenderer>().material = black;
                puzzle1.transform.GetChild(3).GetComponent<MeshRenderer>().material = black;
                puzzle1.transform.GetChild(5).GetComponent<MeshRenderer>().material = black;
                puzzle1.transform.GetChild(8).GetComponent<MeshRenderer>().material = black;
                puzzle1.transform.GetChild(12).GetComponent<MeshRenderer>().material = black;
                puzzle1.transform.GetChild(19).GetComponent<MeshRenderer>().material = black;
                puzzle1.transform.GetChild(26).GetComponent<MeshRenderer>().material = black;
                puzzle1.transform.GetChild(28).GetComponent<MeshRenderer>().material = black;
                puzzle1.transform.GetChild(32).GetComponent<MeshRenderer>().material = black;
                puzzle1.transform.GetChild(34).GetComponent<MeshRenderer>().material = black;
                puzzle1.transform.GetChild(30).GetComponent<MeshRenderer>().material = bluee;
                puzzle1.transform.GetChild(14).GetComponent<MeshRenderer>().material = red;
                puzzle1.transform.GetChild(10).GetComponent<MeshRenderer>().material = deepOrange;
                puzzle1.transform.GetChild(38).GetComponent<MeshRenderer>().material = deepOrange;
                puzzle1.transform.GetChild(17).GetComponent<MeshRenderer>().material = orange;
                puzzle1.transform.GetChild(21).GetComponent<MeshRenderer>().material = green;
                puzzle1.transform.GetChild(36).GetComponent<MeshRenderer>().material = green;
                puzzle1.transform.GetChild(24).GetComponent<MeshRenderer>().material = beige;

                puzzle2.transform.GetChild(0).GetComponent<MeshRenderer>().material = sphereRed;
                puzzle2.transform.GetChild(1).GetComponent<MeshRenderer>().material = stringBrown;
                puzzle2.transform.GetChild(4).GetComponent<MeshRenderer>().material = stringBrown;
                puzzle2.transform.GetChild(15).GetComponent<MeshRenderer>().material = stringBrown;
                puzzle2.transform.GetChild(18).GetComponent<MeshRenderer>().material = stringBrown;
                puzzle2.transform.GetChild(30).GetComponent<MeshRenderer>().material = stringBrown;
                puzzle2.transform.GetChild(34).GetComponent<MeshRenderer>().material = stringBrown;
                puzzle2.transform.GetChild(40).GetComponent<MeshRenderer>().material = stringBrown;
                puzzle2.transform.GetChild(42).GetComponent<MeshRenderer>().material = stringBrown;
                puzzle2.transform.GetChild(46).GetComponent<MeshRenderer>().material = stringBrown;
                puzzle2.transform.GetChild(48).GetComponent<MeshRenderer>().material = stringBrown;
                puzzle2.transform.GetChild(3).GetComponent<MeshRenderer>().material = black;
                puzzle2.transform.GetChild(20).GetComponent<MeshRenderer>().material = black;
                puzzle2.transform.GetChild(22).GetComponent<MeshRenderer>().material = black;
                puzzle2.transform.GetChild(24).GetComponent<MeshRenderer>().material = black;
                puzzle2.transform.GetChild(37).GetComponent<MeshRenderer>().material = black;
                puzzle2.transform.GetChild(6).GetComponent<MeshRenderer>().material = beige;
                puzzle2.transform.GetChild(31).GetComponent<MeshRenderer>().material = beige;
                puzzle2.transform.GetChild(33).GetComponent<MeshRenderer>().material = beige;
                puzzle2.transform.GetChild(17).GetComponent<MeshRenderer>().material = brown;
                puzzle2.transform.GetChild(32).GetComponent<MeshRenderer>().material = yelloww;
                puzzle2.transform.GetChild(8).GetComponent<MeshRenderer>().material = deepOrange;
                puzzle2.transform.GetChild(9).GetComponent<MeshRenderer>().material = deepOrange;
                puzzle2.transform.GetChild(10).GetComponent<MeshRenderer>().material = deepOrange;
                puzzle2.transform.GetChild(38).GetComponent<MeshRenderer>().material = deepOrange;

                ring.transform.GetChild(0).GetComponent<MeshRenderer>().material = bluee;
                ring.transform.GetChild(1).GetComponent<MeshRenderer>().material = bluee;
                ring.transform.GetChild(7).GetComponent<MeshRenderer>().material = bluee;
                ring.transform.GetChild(8).GetComponent<MeshRenderer>().material = bluee;
                ring.transform.GetChild(11).GetComponent<MeshRenderer>().material = bluee;
                ring.transform.GetChild(12).GetComponent<MeshRenderer>().material = bluee;
                ring.transform.GetChild(18).GetComponent<MeshRenderer>().material = bluee;
                ring.transform.GetChild(19).GetComponent<MeshRenderer>().material = bluee;
                ring.transform.GetChild(2).GetComponent<MeshRenderer>().material = black;
                ring.transform.GetChild(6).GetComponent<MeshRenderer>().material = black;
                ring.transform.GetChild(13).GetComponent<MeshRenderer>().material = black;
                ring.transform.GetChild(15).GetComponent<MeshRenderer>().material = black;
                ring.transform.GetChild(17).GetComponent<MeshRenderer>().material = black;
                ring.transform.GetChild(3).GetComponent<MeshRenderer>().material = sphereRed;
                ring.transform.GetChild(16).GetComponent<MeshRenderer>().material = sphereRed;
                ring.transform.GetChild(4).GetComponent<MeshRenderer>().material = yellowStick;
                ring.transform.GetChild(5).GetComponent<MeshRenderer>().material = yellowStick;
                ring.transform.GetChild(14).GetComponent<MeshRenderer>().material = yellowStick;
                ring.transform.GetChild(9).GetComponent<MeshRenderer>().material = gray;
                ring.transform.GetChild(10).GetComponent<MeshRenderer>().material = gray;

                stick_M.transform.GetComponent<MeshRenderer>().material = _90out;
                stick_M1.transform.GetComponent<MeshRenderer>().material = black;
                stick_M2.transform.GetComponent<MeshRenderer>().material = black;
                stick_M3.transform.GetComponent<MeshRenderer>().material = black;
                stick_M4.transform.GetComponent<MeshRenderer>().material = deepOrange;
                stick_M5.transform.GetComponent<MeshRenderer>().material = black;
                stick_M6.transform.GetComponent<MeshRenderer>().material = black;
                stick_M7.transform.GetComponent<MeshRenderer>().material = black;
                stick_M8.transform.GetComponent<MeshRenderer>().material = black;
                stick_M9.transform.GetComponent<MeshRenderer>().material = black;
                stick_M10.transform.GetComponent<MeshRenderer>().material = black;
                stick_M11.transform.GetComponent<MeshRenderer>().material = stringBrown;
                stick_M12.transform.GetComponent<MeshRenderer>().material = stringBrown;
                stick_M13.transform.GetComponent<MeshRenderer>().material = stringBrown;
                sitck1_M_14.transform.GetComponent<MeshRenderer>().material = stringBrown;
                stick1_L.transform.GetComponent<MeshRenderer>().material = _90out;
                stick2_L.transform.GetComponent<MeshRenderer>().material = _90out;
                stick3_L.transform.GetComponent<MeshRenderer>().material = _90out;
                stick4_L.transform.GetComponent<MeshRenderer>().material = _90out;
                stick5_L.transform.GetComponent<MeshRenderer>().material = stickMat;
                stick6_L.transform.GetComponent<MeshRenderer>().material = stickMat;
                _90.transform.GetChild(0).GetComponent<MeshRenderer>().material = _90out;
                cube_3.transform.GetComponent<MeshRenderer>().material = black;
                _4cube.transform.GetChild(6).GetComponent<MeshRenderer>().material = white;
                _4cube.transform.GetChild(7).GetComponent<MeshRenderer>().material = redHeart;
                _4cube.transform.GetChild(8).GetComponent<MeshRenderer>().material = white;
                _4cube.transform.GetChild(9).GetComponent<MeshRenderer>().material = red;
                front_stick1.transform.GetComponent<MeshRenderer>().material = brown;
                front_stick2.transform.GetComponent<MeshRenderer>().material = sphereRed;
                stick1_yellow_M.transform.GetComponent<MeshRenderer>().material = yellowStick;
                longStick.transform.GetChild(0).GetComponent<MeshRenderer>().material = sphereRed;
                longStick.transform.GetChild(1).GetComponent<MeshRenderer>().material = black;
                longStick.transform.GetChild(2).GetComponent<MeshRenderer>().material = beige;
                longStick.transform.GetChild(3).GetComponent<MeshRenderer>().material = white;
                longStick.transform.GetChild(4).GetComponent<MeshRenderer>().material = black;
                longStick.transform.GetChild(5).GetComponent<MeshRenderer>().material = black;
                longStick.transform.GetChild(6).GetComponent<MeshRenderer>().material = black;
                longStick.transform.GetChild(7).GetComponent<MeshRenderer>().material = white;
                longStick.transform.GetChild(8).GetComponent<MeshRenderer>().material = black;
                longStick.transform.GetChild(9).GetComponent<MeshRenderer>().material = white;
                longStick.transform.GetChild(10).GetComponent<MeshRenderer>().material = black;
                longStick.transform.GetChild(11).GetComponent<MeshRenderer>().material = white;
                longStick.transform.GetChild(12).GetComponent<MeshRenderer>().material = black;
                longStick.transform.GetChild(13).GetComponent<MeshRenderer>().material = white;
                longStick.transform.GetChild(14).GetComponent<MeshRenderer>().material = black;
                stick_bottom.transform.GetComponent<MeshRenderer>().material = black;
                stick_bottom2.transform.GetComponent<MeshRenderer>().material = black;
                stick_bottom3.transform.GetComponent<MeshRenderer>().material = black;
                brownStick_bottom.transform.GetComponent<MeshRenderer>().material = brown;
                brownStick_bottom2.transform.GetComponent<MeshRenderer>().material = brown;
                blackStick_bottom.transform.GetComponent<MeshRenderer>().material = black;
                blackStick_bottom.transform.GetChild(0).GetComponent<MeshRenderer>().material = black;
                blackStick_bottom.transform.GetChild(1).GetComponent<MeshRenderer>().material = black;
                blackStick_bottom_1.transform.GetComponent<MeshRenderer>().material = black;
                blackStick_bottom_1.transform.GetChild(0).GetComponent<MeshRenderer>().material = black;
                blackStick_bottom_1.transform.GetChild(1).GetComponent<MeshRenderer>().material = black;
                black_cube.transform.GetComponent<MeshRenderer>().material = black;
                blackCube2.transform.GetComponent<MeshRenderer>().material = black;
                blackCube3.transform.GetComponent<MeshRenderer>().material = black;
                blackCube4.transform.GetComponent<MeshRenderer>().material = black;
                redCube2.transform.GetComponent<MeshRenderer>().material = redHeart;
                top_blueSphere.transform.GetComponent<MeshRenderer>().material = bluee;
                top_redSphere.transform.GetComponent<MeshRenderer>().material = sphereRed;
                puzzle_grayCube.transform.GetComponent<MeshRenderer>().material = gray;
                sphere_beige.transform.GetComponent<MeshRenderer>().material = beige;
                sphere_pupple.transform.GetComponent<MeshRenderer>().material = spherePupple;
                puzzleSphere_blue1.transform.GetComponent<MeshRenderer>().material = blue_sphere;
                puzzleSphere_blue2.transform.GetComponent<MeshRenderer>().material = spherePupple;
                puzzleSphere_orange.transform.GetComponent<MeshRenderer>().material = triangleOrange;
                top_triangle.transform.GetComponent<MeshRenderer>().material = triangleOrange;
                right_bottom_triangle.transform.GetComponent<MeshRenderer>().material = deepOrange;
                red_Cube.transform.GetChild(4).GetComponent<MeshRenderer>().material = sphereRed;
                for(int i=0;i<2;i++)
                {
                    blue_triangle.transform.GetChild(i).GetComponent<MeshRenderer>().material = bluee;
                }
                under_wave.transform.GetChild(0).GetComponent<MeshRenderer>().material = stringBrown;
                green_and_orange.transform.GetChild(0).GetComponent<MeshRenderer>().material = deepOrange;
                green_and_orange.transform.GetChild(1).GetComponent<MeshRenderer>().material = green;
                for(int i=0;i<4;i++)
                {
                    brownWave.transform.GetChild(i).GetComponent<MeshRenderer>().material = stringBrown;
                }
                color_wave.transform.GetChild(0).GetComponent<MeshRenderer>().material = black;
                color_wave.transform.GetChild(1).GetComponent<MeshRenderer>().material = orange;
                color_wave.transform.GetChild(2).GetComponent<MeshRenderer>().material = red;
                color_wave.transform.GetChild(3).GetComponent<MeshRenderer>().material = black;
                red_wave.transform.GetComponent<MeshRenderer>().material = sphereRed;
                yellowCube.transform.GetChild(0).GetComponent<MeshRenderer>().material = redSpYellow;
                puzzle_blue.transform.GetChild(0).GetComponent<MeshRenderer>().material = yelloww;
                puzzle_blue.transform.GetChild(1).GetComponent<MeshRenderer>().material = bluee;
                arrowBackground.transform.GetComponent<MeshRenderer>().material = beige;
                spring_with_stick.transform.GetChild(0).GetComponent<MeshRenderer>().material = black;
                spring_with_stick.transform.GetChild(1).GetComponent<MeshRenderer>().material = black;
                spring_with_stick.transform.GetChild(2).GetComponent<MeshRenderer>().material = black;
            }

            Character.transform.position = Vector3.MoveTowards(Character.transform.position, new Vector3(0, 0, -5), 1.0f * Time.deltaTime);
            ObjectToFinal(stick_M, new Vector3(17, 11.44f, 48.71f), new Vector3(18.935f, -127.08f, 91.59f), new Vector3(0.3f, 0.3f, 10));
            ObjectToFinal(stick_M1, new Vector3(16.52f, 13.36f, 48.27f), new Vector3(23.649f, -126.94f, 91.65f), new Vector3(0.2f, 0.2f, 25));
            ObjectToFinal(stick_M2, new Vector3(17.51f, 15.39f, 48.96f), new Vector3(21.378f, -127.01f, 91.623f), new Vector3(0.2f, 0.2f, 20));
            ObjectToFinal(stick_M3, new Vector3(11.94f, 13.94f, 44.72f), new Vector3(21.378f, -127.01f, 91.623f), new Vector3(0.2f, 0.2f, 25));
            ObjectToFinal(stick_M4, new Vector3(11.98f, 13.81f, 45f), new Vector3(21.378f, -127.01f, 91.623f), new Vector3(0.2f, 0.2f, 25));
            ObjectToFinal(stick_M5, new Vector3(8.47f, 13.58f, 42.06f), new Vector3(21.378f, -127.01f, 91.623f), new Vector3(0.1f, 0.1f, 20));
            ObjectToFinal(stick_M6, new Vector3(8.36f, 13.95f, 41.96f), new Vector3(21.378f, -127.01f, 91.623f), new Vector3(0.2f, 0.2f, 20));
            ObjectToFinal(stick_M7, new Vector3(12.53f, 26.73f, 55.34f), new Vector3(-6.697f, -127.78f, 91.521f), new Vector3(0.1f, 0.1f, 20));
            ObjectToFinal(stick_M8, new Vector3(11.32f, 25.54f, 54.45f), new Vector3(-9.88f, -116.25f, 89.54f), new Vector3(0.1f, 0.1f, 20));
            ObjectToFinal(stick_M9, new Vector3(31.42f, 39.85f, 83.37f), new Vector3(90, 90, 0), new Vector3(0.1f, 0.1f, 15));
            ObjectToFinal(stick_M10, new Vector3(32.01f, 39.85f, 83.37f), new Vector3(90, 90, 0), new Vector3(0.1f, 0.1f, 15));
            ObjectToFinal(stick_M11, new Vector3(32.01f, 45.78f, 83.37f), new Vector3(0, 90, 0), new Vector3(0.1f, 0.1f, 5));
            ObjectToFinal(stick_M12, new Vector3(32.01f, 45.27f, 83.37f), new Vector3(0, 90, 0), new Vector3(0.1f, 0.1f, 5));
            ObjectToFinal(stick_M13, new Vector3(32.01f, 34.2f, 83.37f), new Vector3(0, 90, 0), new Vector3(0.1f, 0.1f, 5));
            ObjectToFinal(puzzle1, new Vector3(-3.76f, -3.03f, 10), new Vector3(0, 180, 13.525f), new Vector3(0.7f, 0.7f, 0.7f));
            ObjectToFinal(puzzle2, new Vector3(20, 10, 30), new Vector3(10, -90, 14), new Vector3(1, 1, 1));
            ObjectToFinal(half, new Vector3(3.38f, 0.145f, 3.076f), new Vector3(-104.39f, 89.956f, 113.72f), new Vector3(0.15f, 0.15f, 0.15f));
            ObjectToFinal(ring, new Vector3(1.626f, 0.187f, 0.607f), new Vector3(90, 0, 0), new Vector3(0.32f, 0.32f, 0.32f));
            ObjectToFinal(eye, new Vector3(1.46f, 0.16f, 0.11f), new Vector3(0, 190, 0), new Vector3(0.2f, 0.2f, 0.2f));
            ObjectToFinal(_90, new Vector3(14.9f, 13.75f, 60), new Vector3(-10, 90, 0), new Vector3(1.5f, 1.5f, 1.5f));
            ObjectToFinal(puzzle_blue, new Vector3(23.6f, 16.24f, 28.81f), new Vector3(0, 0, 0), new Vector3(0.6f, 0.6f, 0.1f));
            ObjectToFinal(puzzle_grayCube, new Vector3(23.43f, 13.33f, 30.59f), new Vector3(-12.322f, 32.634f, 27.274f), new Vector3(0.8f, 0.8f, 0.8f));
            ObjectToFinal(brownWave, new Vector3(3.46f, -5.57f, 23), new Vector3(0, 0, 90), new Vector3(1.3f, 1.3f, 1.3f));
            ObjectToFinal(sitck1_M_14, new Vector3(32.01f, 33.69f, 83.37f), new Vector3(0, 90, 0), new Vector3(0.1f, 0.1f, 5));
            ObjectToFinal(flat_circle5, new Vector3(-2.5f, 4, 15), new Vector3(0, 90, 0), new Vector3(1.2f, 1.2f, 1.2f));
            ObjectToFinal(flat_circle5_in_background, new Vector3(14.3f, 25.29f, 62), new Vector3(0, 90, 0), new Vector3(2, 2, 2));
            ObjectToFinal(cube_3, new Vector3(4, -2.2f, 5), new Vector3(0, 90, 0), new Vector3(0.05f, 0.05f, 2));
            ObjectToFinal(red_wave, new Vector3(11.27f, 9.87f, 44.34f), new Vector3(2.413f, -49.029f, 108.852f), new Vector3(2, 3, 2));
            ObjectToFinal(green_and_orange, new Vector3(16.53f, -1.04f, 52.7f), new Vector3(0, 180, 10.565f), new Vector3(5, 5, 5));
            ObjectToFinal(arrow, new Vector3(4.55f, -4, 16.86f), new Vector3(0, 0, 0), new Vector3(2, 2.5f, 2));
            ObjectToFinal(arrowBackground, new Vector3(14.17f, 16.19f, 61.8f), new Vector3(-90, -90, 90), new Vector3(11.169f, 0.1f, 24.9657f));
            ObjectToFinal(puzzle_white1, new Vector3(-1.13f, 1.39f, 15), new Vector3(0, 0, 0), new Vector3(0.4f, 0.4f, 0.4f));
            ObjectToFinal(puzzle_white2, new Vector3(-3.17f, 0.48f, 15), new Vector3(0, 0, 0), new Vector3(0.4f, 0.4f, 0.4f));
            ObjectToFinal(puzzlewhite2_1, new Vector3(-6.865f, -1.323f, 12), new Vector3(0, 0, 0), new Vector3(1, 1, 1));
            ObjectToFinal(puzzle_white2_2, new Vector3(25.32f, 1.35f, 56.99f), new Vector3(0, 0, 0), new Vector3(3, 3, 3));
            ObjectToFinal(puzzle_whilte2_3, new Vector3(25.6f, 36.8f, 79.5f), new Vector3(0, 0, 0), new Vector3(1.5f, 1.5f, 1.5f));
            ObjectToFinal(puzzlewhilte2_4, new Vector3(70.31f, 40.43f, 79.5f), new Vector3(-8.286f, 33.889f, 0), new Vector3(1.5f, 1.5f, 1.5f));
            ObjectToFinal(blue, new Vector3(-1.2f, -4.5f, 5), new Vector3(0, 0, 0), new Vector3(0.5f, 0.5f, 0.5f));
            ObjectToFinal(yellow, new Vector3(-7, -2.5f, 5), new Vector3(0, -30, 0), new Vector3(0.5f, 0.5f, 0.5f));
            ObjectToFinal(_4cube, new Vector3(4.67f, 1.679f, 0.72f), new Vector3(0, 26.53f, 0), new Vector3(2, 2, 2));
            ObjectToFinal(red_sphere, new Vector3(-9.34f, 2.88f, 12), new Vector3(0, 0, 0), new Vector3(1.2f, 1.2f, 1.2f));
            ObjectToFinal(Heeart, new Vector3(-9.84f, 5.08f, 10), new Vector3(200, -90, -20), new Vector3(3, 3, 3));
            ObjectToFinal(under_wave, new Vector3(5.4f, -4, 22.71f), new Vector3(0, 90, 0), new Vector3(0.05f, 0.05f, 6));
            ObjectToFinal(right_bottom_triangle, new Vector3(10.3f, -4, 15.55f), new Vector3(0, 0, 90), new Vector3(1.5f, 1, 1));
            ObjectToFinal(smile, new Vector3(3.626f, -0.213f, 5.107f), new Vector3(300, 15, -50), new Vector3(0, 0.025f, 0.03f));
            ObjectToFinal(color_wave, new Vector3(2.5f, -4, 23.01f), new Vector3(0, -90, 0), new Vector3(1, 1, 1));
            ObjectToFinal(spring_with_stick, new Vector3(-26, -1.3f, 34.26f), new Vector3(10, 176, 70), new Vector3(1.2f, 1.5f, 1.2f));
            ObjectToFinal(longStick, new Vector3(3.88f, -3.43f, 3.99f), new Vector3(30.906f, -140.147f, 147.765f), new Vector3(1, 1, 1));
            ObjectToFinal(sphere_beige, new Vector3(12.5f, -6, 17), new Vector3(0, 0, 0), new Vector3(3, 3, 3));
            ObjectToFinal(sphere_pupple, new Vector3(15.4f, -8.97f, 35.51f), new Vector3(0, 0, 0), new Vector3(3, 3, 3));
            ObjectToFinal(top_triangle, new Vector3(15.81f, 32.14f, 61), new Vector3(-108.37f, 0, 0), new Vector3(2.7f, 0.1f, 2.2516f));
            ObjectToFinal(red_Cube, new Vector3(5.6f, -2.5f, 5.5f), new Vector3(0, 30, 0), new Vector3(0.3f, 0.3f, 0.3f));
            ObjectToFinal(stick1_L, new Vector3(-13, 20, 49.9f), new Vector3(0, 90, 0), new Vector3(0.3f, 0.3f, 8));
            ObjectToFinal(stick2_L, new Vector3(-15, 20, 50), new Vector3(90, 0, -90), new Vector3(0.3f, 0.3f, 18));
            ObjectToFinal(stick5_L, new Vector3(-15, 22, 50), new Vector3(0, 90, 0), new Vector3(0.3f, 0.3f, 8));
            ObjectToFinal(stick6_L, new Vector3(-12, 25, 50), new Vector3(30, 90, 0), new Vector3(0.3f, 0.3f, 15));
            ObjectToFinal(left_blackmodel, new Vector3(-16, 15, 45), new Vector3(250, 15, -50), new Vector3(0.7f, 0.7f, 0.7f));
            ObjectToFinal(blackStick_bottom, new Vector3(2.21f, -2.67f, 3.61f), new Vector3(10.243f, -134.42f, 90.28f), new Vector3(0.025f, 0.025f, 3));
            ObjectToFinal(blackStick_bottom_1, new Vector3(2.25f, -3.03f, 7.8f), new Vector3(19.932f, -137.09f, 89.408f), new Vector3(0.03f, 0.03f, 4));
            ObjectToFinal(puzzleSphere_blue1, new Vector3(23.4882f, 14.0583f, 29.5049f), new Vector3(10, -90, 14), new Vector3(0.5f, 2, 2));
            ObjectToFinal(puzzleSphere_blue2, new Vector3(19.95f, 8.24f, 30.65f), new Vector3(10, -90, 14), new Vector3(1,2,2));
            ObjectToFinal(puzzleSphere_orange, new Vector3(18.336f, 15.406f, 28.951f), new Vector3(9.143f, -86.587f, 14.568f), new Vector3(0.5f, 2, 2));
            ObjectToFinal(puzzle_torus, new Vector3(18.2938f, 15.3568f, 28.9096f), new Vector3(-23.385f, 15.181f, 27.358f), new Vector3(1.1f, 1.2f, 0));
            ObjectToFinal(stick1_yellow_M, new Vector3(17.12f, 11.24f, 48.79f), new Vector3(18.935f, -127.08f, 91.597f), new Vector3(0.2f, 0.2f, 12));
            ObjectToFinal(stick_bottom, new Vector3(4.53f, -2.93f, 5), new Vector3(0, 90, 0), new Vector3(0.05f, 0.05f, 2.5f));
            ObjectToFinal(stick_bottom2, new Vector3(0.01f, -4.7f, 7.26f), new Vector3(0, 90, 0), new Vector3(0.05f, 0.05f, 1.5f));
            ObjectToFinal(stick_bottom3, new Vector3(0.03f, -4.09f, 7.58f), new Vector3(0, 90, 0), new Vector3(0.05f, 0.05f, 1.5f));
            ObjectToFinal(brownStick_bottom, new Vector3(-1.4f, -3.7f, 3.35f), new Vector3(20.875f, -127.03f, 91.617f), new Vector3(0.02f, 0.02f, 2.5f));
            ObjectToFinal(brownStick_bottom2, new Vector3(-1.4f, -3, 3.35f), new Vector3(10.243f, -134.42f, 90.28f), new Vector3(0.025f, 0.025f, 3));
            ObjectToFinal(redCube2, new Vector3(16.92f, 14.23f, 30.27f), new Vector3(-16.967f, 19.875f, -0.877f), new Vector3(3, 2, 2));
            ObjectToFinal(front_stick1, new Vector3(0, 0, -1), new Vector3(10.243f, -134.42f, 90.28f), new Vector3(0.05f, 0.05f, 2));
            ObjectToFinal(front_stick2, new Vector3(0, -0.2f, -1), new Vector3(10, -150, 90.28f), new Vector3(0.05f, 0.05f, 2));
            ObjectToFinal(black_cube, new Vector3(24.15f, 12.05f, 30.46f), new Vector3(-12.322f, 32.634f, 27.274f), new Vector3(0.8f, 0.8f, 0.8f));
            ObjectToFinal(blackCube2, new Vector3(26.77f, 16.58f, 30.51f), new Vector3(-12.322f, 32.634f, 27.274f), new Vector3(0.6f, 0.6f, 0.6f));
            ObjectToFinal(blackCube3, new Vector3(27.18f, 15.47f, 30.53f), new Vector3(-12.322f, 32.634f, 27.274f), new Vector3(0.7f, 0.7f, 0.7f));
            ObjectToFinal(blackCube4, new Vector3(26.38f, 18.17f, 30.34f), new Vector3(-12.322f, 32.634f, 27.274f), new Vector3(0.6f, 0.6f, 0.6f));
            ObjectToFinal(top_blueSphere, new Vector3(7.48f, 31.67f, 52.61f), new Vector3(-9.882f, -116.25f, 89.544f), new Vector3(3, 3, 3));
            ObjectToFinal(top_redSphere, new Vector3(2, 20.11f, 49.8f), new Vector3(-9.882f, -116.25f, 89.544f), new Vector3(2.5f, 2.5f, 2.5f));
            ObjectToFinal(yellowCube, new Vector3(56.33f, 49.17f, 83.37f), new Vector3(0, 118.206f, -13.651f), new Vector3(0.5f, 3, 3));
            ObjectToFinal(blue_triangle, new Vector3(-6.02f, 0.92f, 55), new Vector3(0, 0, -1.082f), new Vector3(11.7874f, 11.7874f, 11.7874f));
            ObjectToFinal(stick3_L, new Vector3(0.55f, 5.43f, 46), new Vector3(35, 90, 0), new Vector3(0.3f, 0.3f, 35));
            ObjectToFinal(stick4_L, new Vector3(-17.75f, 6.43f, 46), new Vector3(-66.241f, 90, 0), new Vector3(0.3f, 0.3f, 20));
            ObjectToFinal(colorRing1, new Vector3(1.127f, 0.309f, -1.146f), new Vector3(0, 0, 0), new Vector3(0.045f, 0.03f, 0.058f));
            ObjectToFinal(colorRing2, new Vector3(1.564f, 0.426f, -1.152f), new Vector3(0, 0, -90.805f), new Vector3(0.045f, 0.03f, 0.058f));
            ObjectToFinal(colorRing3, new Vector3(1.776f, 0.074f, -1.152f), new Vector3(0, 0, -182.79f), new Vector3(0.045f, 0.03f, 0.058f));
            ObjectToFinalLocal(puzzle2.transform.GetChild(2).gameObject, new Vector3(0.79f, 2.95f, 1.91f), new Vector3(-90, 0, 0));
            ObjectToFinalLocal(puzzle2.transform.GetChild(8).gameObject, new Vector3(0.69f, -0.52f, 0.02f), new Vector3(-90, 0, 0));
            ObjectToFinalLocal(puzzle2.transform.GetChild(9).gameObject, new Vector3(0.72f, -1.06f, 0.96f), new Vector3(-90, 0, 0));
            ObjectToFinalLocal(puzzle2.transform.GetChild(23).gameObject, new Vector3(0.75f, 4.186f, 0.96f), new Vector3(-90, 0, 0));
            ObjectToFinalLocal(puzzle2.transform.GetChild(24).gameObject, new Vector3(0.8f, 3.43f, 0.89f), new Vector3(-90, 0, 0));
            ObjectToFinalLocal(puzzle2.transform.GetChild(32).gameObject, new Vector3(0.36f, 5.01f, 0.99f), new Vector3(-90, 0, 0));
            ObjectToFinalLocal(puzzle2.transform.GetChild(37).gameObject, new Vector3(-0.78f, 4.61f, -3.29f), new Vector3(-90, 0, 0));
            ObjectToFinalLocal(puzzle2.transform.GetChild(39).gameObject, new Vector3(0.37f, 2.58f, -1.59f), new Vector3(-90, 0, 0));
            ObjectToFinalLocal(puzzle2.transform.GetChild(44).gameObject, new Vector3(0.36f, 5.02f, -1.49f), new Vector3(-90, 0, 0));
            ObjectToFinalLocal(brownWave.transform.GetChild(0).gameObject, new Vector3(0, 0, 0), new Vector3(0, 0, 0));
            ObjectToFinalLocal(brownWave.transform.GetChild(1).gameObject, new Vector3(0, -2.15f, 0), new Vector3(0, 0, 0));
            ObjectToFinalLocal(brownWave.transform.GetChild(2).gameObject, new Vector3(-1.1f, -3.44f, 0), new Vector3(0, 0, 0));
            ObjectToFinalLocal(brownWave.transform.GetChild(3).gameObject, new Vector3(-2.22f, -4.59f, 0), new Vector3(0, 0, 0));
            ObjectToFinalLocal(color_wave.transform.GetChild(0).gameObject, new Vector3(0, 0, 0), new Vector3(0, -90, 90));
            ObjectToFinalLocal(color_wave.transform.GetChild(1).gameObject, new Vector3(0, 0, -2), new Vector3(0, -90, 90));
            ObjectToFinalLocal(color_wave.transform.GetChild(2).gameObject, new Vector3(0, 0, -4), new Vector3(0, -90, 90));
            ObjectToFinalLocal(color_wave.transform.GetChild(3).gameObject, new Vector3(0, 0, -6), new Vector3(0, -90, 90));
        }
    }

    void ObjectToFinalLocal(GameObject obj, Vector3 toPos, Vector3 toRot)
    {
        obj.transform.localPosition = Vector3.MoveTowards(obj.transform.localPosition,
            toPos, speed);
        obj.transform.localRotation = Quaternion.Slerp(obj.transform.localRotation,
            Quaternion.Euler(toRot), speed);
    }

    void ObjectToFinal(GameObject obj, Vector3 toPos, Vector3 toRot, Vector3 toScale)
    {
        MoveObject(obj, toPos);
        RotateObject(obj, toRot);

        if (obj.tag == "Background")
        {
            Scale(obj, toScale, 0.03f);
        }

        else if(obj.tag == "Arrow")
        {
            Scale(obj, toScale, 0.015f);
        }

        else if(obj.tag == "stick")
        {
            Scale(obj, toScale, 0.02f);
        }

        else
        {
            Scale(obj, toScale);
        }
    }

    void MoveObject(GameObject obj, Vector3 toPos)
    {
        obj.transform.position = Vector3.MoveTowards(obj.transform.position,
            toPos, speed);
    }

    void RotateObject(GameObject obj, Vector3 toRot)
    {
        obj.transform.rotation = Quaternion.Slerp(obj.transform.rotation,
            Quaternion.Euler(toRot), speed);
    }

    void Scale(GameObject obj, Vector3 toScale)
    {
        if(obj.transform.localScale.x >= toScale.x)
        {
            obj.transform.localScale -= new Vector3(0.001f, 0, 0);
        }

        else
        {
            obj.transform.localScale += new Vector3(0.001f, 0, 0);
        }

        if (obj.transform.localScale.y >= toScale.y)
        {
            obj.transform.localScale -= new Vector3(0, 0.001f, 0);
        }

        else
        {
            obj.transform.localScale += new Vector3(0, 0.001f, 0);
        }

        if (obj.transform.localScale.z >= toScale.z)
        {
            obj.transform.localScale -= new Vector3(0, 0, 0.001f);
        }

        else
        {
            obj.transform.localScale += new Vector3(0, 0, 0.001f);
        }
    }

    void Scale(GameObject obj, Vector3 toScale, float scaleSpeed)
    {
        if (obj.transform.localScale.x >= toScale.x)
        {
            obj.transform.localScale -= new Vector3(scaleSpeed, 0, 0);
        }

        else
        {
            obj.transform.localScale += new Vector3(scaleSpeed, 0, 0);
        }

        if (obj.transform.localScale.y >= toScale.y)
        {
            obj.transform.localScale -= new Vector3(0, scaleSpeed, 0);
        }

        else
        {
            obj.transform.localScale += new Vector3(0, scaleSpeed, 0);
        }

        if (obj.transform.localScale.z >= toScale.z)
        {
            obj.transform.localScale -= new Vector3(0, 0, scaleSpeed);
        }

        else
        {
            obj.transform.localScale += new Vector3(0, 0, scaleSpeed);
        }
    }

    IEnumerator timeChecker()
    {
        while(true)
        {
            time += 0.1f;

            if(time >= 180f)
            {
                timeFin = true;
            }

            if(time>=205f)
            {
                colorBool = true;
            }

            if(time >= 210f)
            {
                SceneManager.LoadScene("Final");
            }

            yield return new WaitForSeconds(0.1f);
        }
    }
}